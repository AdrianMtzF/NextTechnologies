from __future__ import annotations
from sqlalchemy import text
from etl_project.src.db import get_engine

def transform_staging_to_cargo() -> tuple[int, int]:
    engine = get_engine()

    ddl_create = """
    CREATE TABLE IF NOT EXISTS public."Cargo" (
      id           varchar(24)   PRIMARY KEY,
      company_name varchar(130)  NULL,
      company_id   varchar(24)   NOT NULL,
      amount       numeric(20,2) NOT NULL CHECK (amount >= 0),
      status       varchar(30)   NOT NULL,
      created_at   timestamp     NOT NULL,
      updated_at   timestamp     NULL
    );
    """

    ddl_alter_amount = """
    ALTER TABLE public."Cargo"
    ALTER COLUMN amount TYPE numeric(20,2);
    """

    insert_sql = """
    WITH base AS (
      SELECT
        TRIM(id)                       AS id_raw,
        NULLIF(TRIM(name), '')         AS company_name,
        TRIM(company_id)               AS company_id_raw,
        NULLIF(TRIM(amount), '')       AS amount_raw,
        UPPER(TRIM(status))            AS status_norm,
        NULLIF(TRIM(created_at), '')   AS created_at_raw,
        NULLIF(TRIM(paid_at), '')      AS paid_at_raw
      FROM entrada.raw_charges
    ),
    cleaned AS (
      SELECT
        id_raw,
        company_name,
        company_id_raw,
        regexp_replace(amount_raw, '[^0-9\\.-]', '', 'g') AS amount_raw_clean,
        status_norm,
        created_at_raw,
        paid_at_raw
      FROM base
    ),
    casted AS (
      SELECT
        SUBSTRING(id_raw FROM 1 FOR 24)                 AS id,
        company_name,
        SUBSTRING(company_id_raw FROM 1 FOR 24)         AS company_id,
        ROUND((amount_raw_clean)::numeric, 2)           AS amount,
        status_norm                                     AS status,
        (created_at_raw)::timestamp                     AS created_at,
        (paid_at_raw)::timestamp                        AS updated_at
      FROM cleaned
    ),
    filtered AS (
      SELECT *
      FROM casted
      WHERE id IS NOT NULL
        AND company_id IS NOT NULL
        AND amount IS NOT NULL
        AND amount >= 0
        AND ABS(amount) < 1e18
        AND status IS NOT NULL
        AND created_at IS NOT NULL
    )
    INSERT INTO public."Cargo"(id, company_name, company_id, amount, status, created_at, updated_at)
    SELECT id, company_name, company_id, amount, status, created_at, updated_at
    FROM filtered
    ON CONFLICT (id) DO NOTHING;
    """

    with engine.begin() as conn:
        exists = conn.execute(text("SELECT to_regclass('entrada.raw_charges') IS NOT NULL")).scalar_one()
        if not exists:
            raise RuntimeError("No existe entrada.raw_charges. Corre primero: python -m scripts.etl_load")

        conn.execute(text(ddl_create))
        conn.execute(text(ddl_alter_amount))

        conn.execute(text('TRUNCATE TABLE public."Cargo";'))
        result = conn.execute(text(insert_sql))
        inserted = result.rowcount

        total_cargo = conn.execute(text('SELECT COUNT(*) FROM public."Cargo";')).scalar_one()
        total_stg   = conn.execute(text('SELECT COUNT(*) FROM entrada.raw_charges;')).scalar_one()

    print(f'Cargo OK → filas en staging: {total_stg} | filas cargadas a Cargo: {inserted}')
    return inserted, total_cargo

if __name__ == "__main__":
    transform_staging_to_cargo()
