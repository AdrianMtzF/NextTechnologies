from __future__ import annotations
from sqlalchemy import text
from etl_project.src.db import get_engine

def disperse_cargo_to_companies_charges() -> None:
    engine = get_engine()

    ddl = """
    CREATE TABLE IF NOT EXISTS public.companies (
      id   varchar(24) PRIMARY KEY,
      name varchar(130) NULL
    );

    CREATE TABLE IF NOT EXISTS public.charges (
      id          varchar(24) PRIMARY KEY,
      company_id  varchar(24) NOT NULL REFERENCES public.companies(id),
      -- Ajustamos la precisión para evitar overflow
      amount      numeric(20,2) NOT NULL,
      status      varchar(30) NOT NULL,
      created_at  timestamp NOT NULL,
      updated_at  timestamp NULL
    );
    """

    insert_companies = """
    INSERT INTO public.companies(id, name)
    SELECT DISTINCT company_id, company_name
    FROM public."Cargo"
    ON CONFLICT (id) DO NOTHING;
    """

    insert_charges = """
    INSERT INTO public.charges(id, company_id, amount, status, created_at, updated_at)
    SELECT id, company_id, amount, status, created_at, updated_at
    FROM public."Cargo"
    ON CONFLICT (id) DO NOTHING;
    """

    with engine.begin() as conn:
        conn.execute(text(ddl))
        # Reiniciamos datos para que la corrida sea limpia
        conn.execute(text("TRUNCATE TABLE public.charges;"))
        conn.execute(text("TRUNCATE TABLE public.companies CASCADE;"))
        conn.execute(text(insert_companies))
        conn.execute(text(insert_charges))

        total_companies = conn.execute(text("SELECT COUNT(*) FROM public.companies;")).scalar_one()
        total_charges   = conn.execute(text("SELECT COUNT(*) FROM public.charges;")).scalar_one()

    print(f"Dispersión OK → companies: {total_companies} | charges: {total_charges}")
    return total_companies, total_charges

if __name__ == "__main__":
    disperse_cargo_to_companies_charges()
