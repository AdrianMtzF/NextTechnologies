from etl_project.src.etl_load import load_raw_to_staging
from etl_project.src.etl_transform import transform_staging_to_cargo
from etl_project.src.etl_disperse import disperse_cargo_to_companies_charges

if __name__ == "__main__":
    # 1. Carga a staging
    total_staging = load_raw_to_staging()
    print(f"Staging OK → en tabla: {total_staging}")

    # 2. Transformación a Cargo
    inserted_cargo, total_cargo = transform_staging_to_cargo()
    print(f"Cargo OK → filas cargadas a Cargo: {inserted_cargo}")

    # 3. Dispersión a companies + charges
    total_companies, total_charges = disperse_cargo_to_companies_charges()
    print(f"Dispersión OK → companies: {total_companies} | charges: {total_charges}")

    # Resumen final
    print("="*50)
    print("Flujo completado")
    print(f"Staging: {total_staging} | Cargo: {total_cargo} | Companies: {total_companies} | Charges: {total_charges}")
    print("="*50)
