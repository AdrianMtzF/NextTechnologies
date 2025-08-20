# etl_project/src/etl_load.py
from __future__ import annotations
import pandas as pd
from sqlalchemy import text
from etl_project.config.config import settings
from etl_project.config.db import get_engine
from etl_project.model.schemas import RAW_CHARGES_DDL
from etl_project.services.cleaning_service import clean_text

EXPECTED_COLS = ["id", "name", "company_id", "amount", "status", "created_at", "paid_at"]

def load_raw_to_staging() -> int:
    csv_path = settings.csv_path()
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV no encontrado: {csv_path}")

    # 1) Leer CSV y limpiar filas vacías
    df = pd.read_csv(csv_path, dtype=str, encoding="utf-8")
    df = df.replace(r"^\s*$", pd.NA, regex=True).dropna(how="all")

    # 2) Validar columnas
    missing = [c for c in EXPECTED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Faltan columnas en CSV: {missing}. Presentes: {list(df.columns)}")
    df = df[EXPECTED_COLS]

    df["name"] = df["name"].map(clean_text)

    engine = get_engine()

    # 3) Crear tablas si no existen
    with engine.begin() as conn:
        conn.execute(text(RAW_CHARGES_DDL))
        conn.execute(text("TRUNCATE entrada.raw_charges;"))

    # 4) Insertar por lotes
    df.to_sql(
        "raw_charges",
        con=engine,
        schema="entrada",
        if_exists="append",
        index=False,
        method="multi",
        chunksize=2000,
    )

    # 5) Verificar
    with engine.begin() as conn:
        total = conn.execute(text("SELECT COUNT(*) FROM entrada.raw_charges;")).scalar_one()

    print(f"Staging OK → insertadas: {len(df)} | en tabla: {total}")
    return int(total)
