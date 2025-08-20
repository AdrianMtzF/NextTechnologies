# etl_project/src/etl_transform.py
from __future__ import annotations
from sqlalchemy import text
from etl_project.config.db import get_engine
from etl_project.model.schemas import CARGO_DDL, ALTER_CARGO_AMOUNT
from etl_project.model.sql_queries import TRUNCATE_CARGO, INSERT_CARGO

def transform_staging_to_cargo() -> tuple[int, int]:
    engine = get_engine()

    with engine.begin() as conn:
        # Validación
        exists = conn.execute(
            text("SELECT to_regclass('entrada.raw_charges') IS NOT NULL")
        ).scalar_one()
        if not exists:
            raise RuntimeError(
                "No existe entrada.raw_charges. Corre primero: python -m scripts.etl_load"
            )

        # Crear / actualizar tabla Cargo
        conn.execute(text(CARGO_DDL))
        conn.execute(text(ALTER_CARGO_AMOUNT))

        # Limpiar y cargar
        conn.execute(text(TRUNCATE_CARGO))
        result = conn.execute(text(INSERT_CARGO))
        inserted = result.rowcount

        # Métricas
        total_cargo = conn.execute(text('SELECT COUNT(*) FROM public."Cargo";')).scalar_one()
        total_stg   = conn.execute(text('SELECT COUNT(*) FROM entrada.raw_charges;')).scalar_one()

    print(f'Cargo OK → filas en staging: {total_stg} | filas cargadas a Cargo: {inserted}')
    return inserted, total_cargo

if __name__ == "__main__":
    transform_staging_to_cargo()
