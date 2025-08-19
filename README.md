Prueba Técnica – Proceso ETL
Descripción
Este prueba implementa un proceso ETL (Extract, Transform, Load) para cargar, limpiar, transformar y dispersar información de cargos de dos compañías ficticias.
El objetivo es:

Cargar datos crudos desde CSV a una base de datos.


Transformarlos en un esquema estandarizado.


Normalizarlos en entidades (companies, charges).


Crear una vista SQL para analizar el monto total transaccionado por día y compañía.

Tecnologías utilizadas
Python 3.11+


PostgreSQL 15 (Docker)


SQLAlchemy (ORM / conexión a BD)


Pandas (lectura y validación de CSV)


Docker Compose (orquestación de servicios)




Instalación y ejecución

1. Clonar repositorio
git clone git@github.com:AdrianMtzF/NextTecnology.git
cd NextTecnology




2. Crear entorno virtual
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows


3. Instalar dependencias
pip install -r requirements.txt


4. Levantar base de datos con Docker
docker compose up -d



5. Ejecutar pipeline completo

python -m scripts.run_pipeline


Aparecera una salida asi:
Staging OK → insertadas: 10000 | en tabla: 10000
Cargo OK → filas en staging: 10000 | filas cargadas a Cargo: 9992
Dispersión OK → companies: 3 | charges: 9992
==================================================
Pipeline completado
Staging: 10000 | Cargo: 9992 | Companies: 3 | Charges: 9992
==================================================




Estructura del Proyecto
NextTecnology/
├─ .venv/                 # Entorno virtual
├─ data/
│  └─ docs/
│     └─ data_prueba_tecnica.csv   # Dataset original
├─ scripts/
│  └─ run_pipeline.py     # Script principal
├─ src/
│  ├─ config.py           # Configuración general
│  ├─ db.py               # Conexión a la base de datos
│  ├─ etl_load.py         # Carga inicial a tabla staging
│  ├─ etl.py              # Transformaciones de staging → Cargo
│  ├─ etl_disperse.py     # Dispersión Cargo → companies & charges
│  └─ __init__.py
├─ tests/                
├─ docker-compose.yml    
├─ Dockerfile            
├─ requirements.txt      
├─ .env.example          
└─ README.md             





Etapas del ETL
1.1 – Carga de información (Staging)

Los datos crudos del CSV se cargan a la tabla entrada.raw_charges.
Se conserva todo tal cual para mantener trazabilidad.

1.2 – Extracción

El script etl_load.py extrae los datos del CSV con Pandas.
Se insertan en raw_charges.
Se devuelve un conteo de filas cargadas vs existentes.

1.3 – Transformación (Cargo)

Los datos de raw_charges se limpian:
Se eliminan símbolos no numéricos en montos.
Se normalizan IDs (24 caracteres).
Se convierten fechas a timestamp.
Se descartan registros inválidos.
Se cargan en la tabla public."Cargo".

1.4 – Dispersión (Companies y Charges)

Se normalizan las entidades:

companies: catálogo de compañías únicas.
charges: cada cargo con referencia a companies.
Integridad referencial: charges.company_id → companies.id.


1.5 – Vista SQL

Se creó una vista para obtener el monto total transaccionado por compañía y día:
CREATE OR REPLACE VIEW public.v_company_daily_totals AS
SELECT
    c.id                AS company_id,
    c.name              AS company_name,
    DATE(ch.created_at) AS transaction_day,
    SUM(ch.amount)      AS total_amount
FROM public.charges ch
JOIN public.companies c ON c.id = ch.company_id
GROUP BY c.id, c.name, DATE(ch.created_at)
ORDER BY transaction_day, company_name;




Ejemplo de consulta:
SELECT * FROM public.v_company_daily_totals;


Resultado:

Staging: 10,000 filas insertadas.
Cargo: ~9,992 filas válidas después de limpieza.
Companies: 3 compañías únicas.
Charges: 9,992 transacciones limpias.
Vista: montos diarios agregados por compañía.
Decisiones técnicas
Se eligió PostgreSQL por robustez en manejo de tipos, facilidad de modelado relacional y compatibilidad con Docker.


Se utilizó numeric(20,2) para evitar overflow en los montos.


Se normalizó el modelo a 3 tablas (companies, charges, Cargo) para mantener consistencia y facilitar reporting.






Documentación API — Numbers API

Descripción
Esta API está construida con FastAPI y expone endpoints para:
Extraer un número dado por el usuario.


Recuperar un número faltante.


Ejemplo de arquitectura modular con rutas.
Instalación y ejecución

1. Clonar repositorio
git clone git@github.com:AdrianMtzF/NextTecnology.git
cd NextTecnology/api_project



Crear entorno virtual e instalar dependencias( en el dado caso que no lo hayas hecho):
2. Crear entorno virtual
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows


3. Instalar dependencias
pip install -r requirements.txt


4. Levantar base de datos con Docker
docker compose up -d


5. Ejecutar el servidor

uvicorn app.main:app --reload



6. Estructura del proyecto


api_project/
│── app/
│   ├── models/              
│   │   ├── __init__.py
│   │   └── number.py
│   │
│   ├── routes/             
│   │   ├── __init__.py
│   │   └── number_route.py
│   │
│   ├── test/               
│   │   ├── __init__.py
│   │   └── test_number.py
│   │
│   └── main.py             





Endpoints
1. Extraer número
POST  /numbers/extract/

Query Params

number (int, requerido) → número a extraer.

Ejemplo:

curl -X POST "http://127.0.0.1:8000/numbers/extract/?number=20"


Respuesta:

{
  "message": "Número 20 extraído correctamente"
}


2. Número faltante
GET /numbers/missing/


Ejemplo:



 curl -X GET "http://127.0.0.1:8000/numbers/missing/"



Respuesta

 {
  "missing_number": 20
}



3. Reiniciar conjunto
POST /numbers/reset/

{
  "message": "Conjunto reiniciado correctamente"
}





Pruebas

Estando en la carpeta:

cd NextTecnology/api_project



Ejecutar las pruebas unitarias con pytest:

pytest -v



Salida esperada:
app/test/test_number.py::test_extract_number PASSED
app/test/test_number.py::test_missing_number PASSED
app/test/test_number.py::test_invalid_number PASSED
app/test/test_number.py::test_reset_allows_new_extraction PASSED




Tecnologías
Python 3.13
FastAPI
Uvicorn
Pytest
