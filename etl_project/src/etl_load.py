from __future__ import annotations
import pandas as pd
from sqlalchemy import text
from etl_project.src.config import settings
from etl_project.src.db import get_engine

EXPECTED_COLS = ["id", "name", "company_id", "amount", "status", "created_at", "paid_at"]

def load_raw_to_staging() -> int:

    csv_path = settings.csv_path()
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV no encontrado: {csv_path}")

    # 1) Lee y limpia filas vacias
    df = pd.read_csv(csv_path, dtype=str, encoding="utf-8")
    df = df.replace(r"^\s*$", pd.NA, regex=True).dropna(how="all")

    # 2) Valida y reordena las columnas
    missing = [c for c in EXPECTED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Faltan columnas en CSV: {missing}. Presentes: {list(df.columns)}")
    df = df[EXPECTED_COLS]

    engine = get_engine()

    # 3) DDL de staging + truncate
    ddl = """
    CREATE SCHEMA IF NOT EXISTS entrada;

    CREATE TABLE IF NOT EXISTS entrada.raw_charges (
      id          text,
      name        text,
      company_id  text,
      amount      text,
      status      text,
      created_at  text,
      paid_at     text
    );
    """
    with engine.begin() as conn:
        conn.execute(text(ddl))
        conn.execute(text("TRUNCATE entrada.raw_charges;"))

    # 4) Cargar por lotes
    df.to_sql(
        "raw_charges",
        con=engine,
        schema="entrada",
        if_exists="append",
        index=False,
        method="multi",
        chunksize=2000,
    )

    # 5) Verificación
    with engine.begin() as conn:
        total = conn.execute(text("SELECT COUNT(*) FROM entrada.raw_charges;")).scalar_one()

    print(f"Staging OK → insertadas: {len(df)} | en tabla: {total}")
    return int(total)

if __name__ == "__main__":
    load_raw_to_staging()
