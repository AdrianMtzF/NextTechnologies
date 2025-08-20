import pytest
from sqlalchemy import text
from etl_project.src.etl_load import load_raw_to_staging
from etl_project.src.etl_transform import transform_staging_to_cargo
from etl_project.src.etl_disperse import disperse_cargo_to_companies_charges
from etl_project.config.db import get_engine


@pytest.fixture(scope="module")
def db_conn():
    engine = get_engine()
    with engine.begin() as conn:
        yield conn


def test_load_raw_to_staging(db_conn):
    total = load_raw_to_staging()
    count = db_conn.execute(text("SELECT COUNT(*) FROM entrada.raw_charges;")).scalar_one()

    assert total == count
    assert total > 0


def test_transform_staging_to_cargo(db_conn):
    inserted, total_cargo = transform_staging_to_cargo()

    # Debe haber filas en Cargo
    assert inserted > 0
    assert total_cargo == inserted

    #Debe tener fechas y montos válidos
    sample = db_conn.execute(
        text('SELECT amount, created_at FROM public."Cargo" LIMIT 5;')
    ).fetchall()
    for amount, created_at in sample:
        assert amount is not None
        assert created_at is not None


def test_disperse_cargo_to_companies_charges(db_conn):
    total_companies, total_charges = disperse_cargo_to_companies_charges()

    assert total_companies > 0
    assert total_charges > 0

    invalid_refs = db_conn.execute(
        text(
            "SELECT COUNT(*) FROM public.charges ch "
            "LEFT JOIN public.companies c ON ch.company_id = c.id "
            "WHERE c.id IS NULL;"
        )
    ).scalar_one()
    assert invalid_refs == 0
