from __future__ import annotations
from sqlalchemy import text
from etl_project.config.db import get_engine
from etl_project.model.schemas import COMPANIES_AND_CHARGES_DDL
from etl_project.model.sql_queries import TRUNCATE_TABLES, INSERT_COMPANIES, INSERT_CHARGES

def disperse_cargo_to_companies_charges() -> tuple[int, int]:
    engine = get_engine()

    with engine.begin() as conn:
        # Crear tablas
        conn.execute(text(COMPANIES_AND_CHARGES_DDL))

        # Limpiar
        conn.execute(text(TRUNCATE_TABLES))

        # Insertar datos
        conn.execute(text(INSERT_COMPANIES))
        conn.execute(text(INSERT_CHARGES))

        # Verificar
        total_companies = conn.execute(text("SELECT COUNT(*) FROM public.companies;")).scalar_one()
        total_charges   = conn.execute(text("SELECT COUNT(*) FROM public.charges;")).scalar_one()

    print(f"Dispersión OK → companies: {total_companies} | charges: {total_charges}")
    return total_companies, total_charges

if __name__ == "__main__":
    disperse_cargo_to_companies_charges()
