Repositorio NextTecnology — Prueba Técnica

Este repositorio contiene dos proyectos independientes como parte de una prueba técnica:

ETL Project (etl_project/) → Implementa un pipeline de extracción, transformación y carga de datos.

API Project (api_project/) → Implementa una API REST con FastAPI para gestión de números.

Ambos proyectos comparten:

Un único entorno virtual (.venv/).

Un único archivo de dependencias (requirements.txt).

Por lo tanto, no es necesario instalar dependencias dos veces. Una vez creado y activado el entorno e instaladas las librerías, se puede ejecutar tanto el pipeline ETL como la API.

Prueba Técnica – Proceso ETL
Descripción
Este proyecto implementa un proceso ETL (Extract, Transform, Load) para cargar, limpiar, transformar y normalizar información de cargos de dos compañías ficticias.
Objetivos:
Cargar datos crudos desde un CSV hacia una base de datos.


Transformarlos a un esquema estandarizado.


Normalizarlos en entidades (companies, charges).


Crear una vista SQL para analizar el monto total transaccionado por compañía y día.


Tecnologías utilizadas
Python 3.13


PostgreSQL 15 (contenedor Docker)


SQLAlchemy (ORM / conexión a BD)


Pandas (lectura y validación de CSV)


Docker Compose (orquestación de servicios)



Instalación y ejecución
1. Clonar el repositorio
git clone git@github.com:AdrianMtzF/NextTecnology.git
cd NextTecnology





2. Crear entorno virtual
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows



3. Instalar dependencias
pip install -r requirements.txt



4. Configurar variables de entorno
Copiar el archivo .env.example como .env y ajustar credenciales si es necesario.
Ejemplo de configuración:
POSTGRES_USER=etl_user
POSTGRES_PASSWORD=etl_pass123
POSTGRES_DB=etl_db
DB_URL=postgresql+psycopg://etl_user:etl_pass123@localhost:5433/etl_db
INPUT_CSV=data/docs/data_prueba_tecnica.csv
POSTGRES_HOST=localhost
POSTGRES_PORT=5433


5. Levantar la base de datos con Docker
docker compose up -d


6. Ejecutar el pipeline completo
Estando en la carpeta NextTecnology: 
cd NextTecnology
python -m etl_project.scripts.run_pipeline


Ejemplo de salida:
Staging OK → insertadas: 10000 | en tabla: 10000
Cargo OK → filas en staging: 10000 | filas cargadas a Cargo: 9992
Dispersión OK → companies: 3 | charges: 9992
==================================================
Pipeline completado
Staging: 10000 | Cargo: 9992 | Companies: 3 | Charges: 9992
==================================================


Estructura del Proyecto
etl_project/
│── config/                   
│   ├── __init__.py
│   ├── config.py             # Configuración de entorno
│   └── db.py                 # Conexión a la base de datos
│
│── data/
│   └── docs/                 # Archivos de entrada 
│       └── __init__.py
│
│── model/
│   ├── __init__.py
│   ├── schemas.py            # Esquemas de validación SQLAlchemy
│   └── sql_queries.py        # Queries SQL centralizadas
│
│── scripts/
│   ├── __init__.py
│   └── run_pipeline.py       # Script principal del pipeline ETL
│
│── services/
│   ├── __init__.py
│   └── cleaning_service.py   # Servicio de limpieza de datos
│
│── src/
│   ├── __init__.py
│   ├── etl_disperse.py       # Dispersión: Cargo → Companies & Charges
│   ├── etl_load.py           # Carga inicial de datos
│   └── etl_transform.py      # Transformaciones de datos
│
│── tests/                    
│   └── __init__.py
│
└── __init__.py






Etapas del ETL
1.1 – Carga de información (Staging)
Se insertan datos crudos del CSV en la tabla entrada.raw_charges.


Se conserva el dataset sin alterar para mantener trazabilidad.




1.2 – Extracción
etl_load.py extrae datos del CSV con Pandas y los inserta en raw_charges.


Devuelve conteo de filas cargadas vs existentes.


1.3 – Transformación (Cargo)
Limpieza de datos desde raw_charges:


Eliminación de símbolos no numéricos en montos.


Normalización de IDs (24 caracteres).


Conversión de fechas a timestamp.


Filtrado de registros inválidos.


Los resultados se cargan en public."Cargo".


1.4 – Dispersión (Companies y Charges)
Normalización de entidades:


companies: catálogo de compañías únicas.


charges: cada cargo con referencia a companies.


Integridad referencial:


charges.company_id → companies.id.


1.5 – Vista SQL (opcional, ejecución manual)
Para reportes, se creó la vista public.v_company_daily_totals que devuelve los montos totales por día y compañía:
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


Resultados esperados
Staging: 10,000 filas insertadas.


Cargo: 9,992 filas válidas después de limpieza.


Companies: 3 compañías únicas.


Charges: 9,992 transacciones limpias.


Vista: totales diarios agregados por compañía.




Decisiones técnicas
PostgreSQL elegido por robustez y fácil integración con Docker.


Uso de numeric(20,2) para evitar problemas de overflow en montos.


Modelo normalizado en 3 tablas (companies, charges, Cargo) para garantizar consistencia y facilitar reportes.


Notas finales
Las credenciales dependen de lo configurado en el archivo .env.


Para ingresar al contenedor(dependiendo de las credenciales):

 docker exec -it etl_postgres psql -U etl_user -d etl_db
Ejecutar la vista SQL solo es necesario una vez, no en cada corrida del pipeline.






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



Crear entorno virtual e instalar dependencias:
2. Crear entorno virtual
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows


Nota: este entorno también se usa para el proyecto ETL, no es necesario crear dos entornos separados.


3. Instalar dependencias
pip install -r requirements.txt


4. Ejecutar el servidor de la API
Desde la carpeta:

cd api_project/:
uvicorn app.main:app --reload



5. Estructura del proyecto


api_project/
│── app/
│   ├── models/               # Modelos de datos
│   │   ├── __init__.py
│   │   └── number.py
│   │
│   ├── routes/               # Definición de rutas
│   │   ├── __init__.py
│   │   └── number_route.py
│   │
│   ├── test/                 # Pruebas unitarias
│   │   ├── __init__.py
│   │   └── test_number.py
│   │
│   └── main.py               # Punto de entrada de la API
│
└── __init__.py

           





Endpoints
1. Extraer número
POST  /numbers/extract/

Query Params

number (int, requerido) → número a extraer.

Ejemplo con curl (Linux/Mac):

curl -X POST "http://127.0.0.1:8000/numbers/extract/?number=20"


Ejemplo con PowerShell (Windows):
Invoke-RestMethod -Uri "http://127.0.0.1:8000/numbers/extract/?number=20" -Method POST



Ejemplo con Postman

Método: POST

URL: http://127.0.0.1:8000/numbers/extract/?number=20
Respuesta:

{
  "message": "Número 20 extraído correctamente"
}



2. Número faltante
GET /numbers/missing/


Ejemplo con curl (Linux/Mac)



 curl -X GET "http://127.0.0.1:8000/numbers/missing/"



Ejemplo con PowerShell (Windows)
Invoke-RestMethod -Uri "http://127.0.0.1:8000/numbers/missing/" -Method GET


Ejemplo con Postman

Método: GET

URL: http://127.0.0.1:8000/numbers/missing/

Respuesta


 {
  "missing_number": 20
}





3. Reiniciar conjunto
POST /numbers/reset/


Ejemplo con curl (Linux/Mac):


curl -X POST "http://127.0.0.1:8000/numbers/reset/"


Ejemplo con PowerShell (Windows):


Invoke-RestMethod -Uri "http://127.0.0.1:8000/numbers/reset/" -Method POST



Ejemplo con Postman
Método: POST


URL: http://127.0.0.1:8000/numbers/reset/

{
  "message": "Conjunto reiniciado correctamente"
}





Pruebas

Estando en:

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
