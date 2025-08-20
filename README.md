
# NextTecnology — Prueba Técnica

Este repositorio contiene dos proyectos independientes desarrollados como parte de una prueba técnica:

- **ETL Project** (`etl_project/`) → Pipeline de extracción, transformación y carga de datos
- **API Project** (`api_project/`) → API REST con FastAPI para gestión de números

## Características Generales

Ambos proyectos comparten:
- Un único entorno virtual (`.venv/`)
- Un único archivo de dependencias (`requirements.txt`)
- Configuración centralizada

**Nota:** No es necesario instalar dependencias dos veces. Una vez configurado el entorno, se pueden ejecutar ambos proyectos.

---

## ETL Project - Proceso ETL

### Descripción

Implementa un proceso ETL (Extract, Transform, Load) para cargar, limpiar, transformar y normalizar información de cargos de dos compañías ficticias.

### Objetivos

- Cargar datos crudos desde un CSV hacia una base de datos
- Transformarlos a un esquema estandarizado
- Normalizarlos en entidades (`companies`, `charges`)
- Crear vista SQL para analizar montos totales por compañía y día

### Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|-----------|---------|-----------|
| Python | 3.13 | Lenguaje principal |
| PostgreSQL | 15 | Base de datos (Docker) |
| SQLAlchemy | - | ORM / conexión a BD |
| Pandas | - | Lectura y validación CSV |
| Docker Compose | - | Orquestación de servicios |

### Instalación y Ejecución

#### 1. Clonar el repositorio

```bash
git clone git@github.com:AdrianMtzF/NextTecnology.git
cd NextTecnology
```

#### 2. Configurar entorno virtual

```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# Linux/Mac
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

#### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

#### 4. Configurar variables de entorno

Copiar `.env.example` como `.env` y ajustar credenciales si es necesario:

```
POSTGRES_USER=etl_user
POSTGRES_PASSWORD=etl_pass123
POSTGRES_DB=etl_db
DB_URL=postgresql+psycopg://etl_user:etl_pass123@localhost:5433/etl_db
INPUT_CSV=data/docs/data_prueba_tecnica.csv
POSTGRES_HOST=localhost
POSTGRES_PORT=5433
```

#### 5. Levantar base de datos

```bash
docker compose up -d
```

#### 6. Ejecutar pipeline completo

```bash
cd NextTecnology
python -m etl_project.scripts.run_pipeline
```

**Salida esperada:**

```
Staging OK → insertadas: 10000 | en tabla: 10000
Cargo OK → filas en staging: 10000 | filas cargadas a Cargo: 9992
Dispersión OK → empresas: 3 | cargos: 9992
==================================================
Pipeline completado
Staging: 10000 | Cargo: 9992 | Companies: 3 | Charges: 9992
==================================================
```

### Estructura del Proyecto

```
etl_project/
├── config/
│   ├── __init__.py
│   ├── config.py              # Configuración de entorno
│   └── db.py                  # Conexión a la base de datos
├── data/
│   └── docs/                  # Archivos de entrada
│       └── __init__.py
├── model/
│   ├── __init__.py
│   ├── schemas.py             # Esquemas de validación SQLAlchemy
│   └── sql_queries.py         # Queries SQL centralizadas
├── scripts/
│   ├── __init__.py
│   └── run_pipeline.py        # Script principal del pipeline ETL
├── services/
│   ├── __init__.py
│   └── cleaning_service.py    # Servicio de limpieza de datos
├── src/
│   ├── __init__.py
│   ├── etl_disperse.py        # Dispersión: Cargo → Companies & Charges
│   ├── etl_load.py           # Carga inicial de datos
│   └── etl_transform.py      # Transformaciones de datos
├── tests/
│   └── __init__.py
└── __init__.py
```

### Etapas del ETL

#### 1. Carga de información (Staging)
- Se insertan datos crudos del CSV en la tabla `entrada.raw_charges`
- Se conserva el dataset sin alterar para mantener trazabilidad

#### 2. Extracción
- `etl_load.py` extrae datos del CSV con Pandas
- Inserta los datos en `raw_charges`
- Devuelve conteo de filas cargadas vs existentes

#### 3. Transformación (Cargo)
Limpieza de datos desde `raw_charges`:
- Eliminación de símbolos no numéricos en montos
- Normalización de IDs (24 caracteres)
- Conversión de fechas a timestamp
- Filtrado de registros inválidos
- Los resultados se cargan en `public."Cargo"`

#### 4. Dispersión (Companies y Charges)
Normalización de entidades:
- `companies`: catálogo de compañías únicas
- `charges`: cada cargo con referencia a companies
- Integridad referencial: `charges.company_id` → `companies.id`

#### 5. Vista SQL (opcional, ejecución manual)
Vista `public.v_company_daily_totals` para reportes con montos totales por día y compañía:

```sql
CREATE OR REPLACE VIEW public.v_company_daily_totals AS
SELECT 
    c.id AS company_id,
    c.name AS company_name,
    DATE(ch.created_at) AS transaction_day,
    SUM(ch.amount) AS total_amount
FROM public.charges ch
JOIN public.companies c ON c.id = ch.company_id
GROUP BY c.id, c.name, DATE(ch.created_at)
ORDER BY transaction_day, company_name;
```

**Ejemplo de consulta:**
```sql
SELECT * FROM public.v_company_daily_totals;
```

### Resultados Esperados

company_id             | company_name    | transaction_day | total_amount
-----------------------|-----------------|-----------------|-------------
cbf1c8b09cd5b549416d49d2 | MiPasajefy     | 2019-01-01      | 4150.04
cbf1c8b09cd5b549416d49d2 | MiPasajefy     | 2019-01-02      | 17044.92
cbf1c8b09cd5b549416d49d2 | MiPasajefy     | 2019-01-03      | 6735.66
8f642dc67fccf861548dfe1c | Muebles chidos | 2019-01-03      | 3199.00
cbf1c8b09cd5b549416d49d2 | MiPasajefy     | 2019-01-04      | 6349.69
cbf1c8b09cd5b549416d49d2 | MiPasajefy     | 2019-01-05      | 5184.97
cbf1c8b09cd5b549416d49d2 | MiPasajefy     | 2019-01-06      | 4005.46
cbf1c8b09cd5b549416d49d2 | MiPasajefy     | 2019-01-07      | 26754.30
cbf1c8b09cd5b549416d49d2 | MiPasajefy     | 2019-01-08      | 5963.77
cbf1c8b09cd5b549416d49d2 | MiPasajefy     | 2019-01-09      | 5859.00


#### Pruebas del ETL

El proyecto incluye pruebas unitarias para validar cada etapa del pipeline ETL.

**Ejecutar las pruebas del ETL:**
```bash
cd NextTecnology
pytest -v etl_project/tests/test_etl.py


Salida esperada:

platform win32 -- Python 3.13.0, pytest-8.2.0, pluggy-1.6.0
cachedir: .pytest_cache
rootdir: C:\Users\Adrian Mtz\PycharmProjects\NextTecnology
plugins: anyio-4.10.0
collected 3 items                                                                                                                                                                                                                  

etl_project/tests/test_etl.py::test_load_raw_to_staging PASSED                    [ 33%]
etl_project/tests/test_etl.py::test_transform_staging_to_cargo PASSED             [ 66%]
etl_project/tests/test_etl.py::test_disperse_cargo_to_companies_charges PASSED   [100%]

3 passed in 9.43s




## Decisiones Técnicas

- **PostgreSQL**: Base de datos robusta con fácil integración en Docker
- **Tipos numéricos**: `numeric(20,2)` para manejar montos sin errores de precisión
- **Estructura normalizada**: 3 tablas separadas para mantener datos consistentes y facilitar consultas

### Notas Adicionales

- Las credenciales dependen de lo configurado en el archivo `.env`
- Para ingresar al contenedor PostgreSQL:
  ```bash
  docker exec -it etl_postgres psql -U etl_user -d etl_db
  ```
- Ejecutar la vista SQL es necesario solo una vez, no en cada corrida del pipeline

---

## API Project - Numbers API

### Descripción

API construida con FastAPI que expone endpoints para:
- Extraer un número dado por el usuario
- Recuperar un número faltante
- Arquitectura modular con rutas

### Instalación y Ejecución

#### 1. Clonar repositorio

```bash
git clone git@github.com:AdrianMtzF/NextTecnology.git
cd NextTecnology/api_project
```

#### 2. Configurar entorno virtual

```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# Linux/Mac
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

**Nota:** Este entorno también se usa para el proyecto ETL, no es necesario crear dos entornos separados.

#### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

#### 4. Ejecutar servidor de la API

```bash
cd api_project/
uvicorn app.main:app --reload
```

### Estructura del Proyecto

```
api_project/
├── app/
│   ├── models/                # Modelos de datos
│   │   ├── __init__.py
│   │   └── number.py
│   ├── routes/                # Definición de rutas
│   │   ├── __init__.py
│   │   └── number_route.py
│   ├── test/                  # Pruebas unitarias
│   │   ├── __init__.py
│   │   └── test_number.py
│   └── main.py               # Punto de entrada de la API
└── __init__.py
```

### Endpoints

#### 1. Extraer número

**POST** `/numbers/extract/`

**Query Params:**
- `number` (int, requerido) → número a extraer

**Ejemplos:**

```bash
# curl (Linux/Mac)
curl -X POST "http://127.0.0.1:8000/numbers/extract/?number=20"

# PowerShell (Windows)
Invoke-RestMethod -Uri "http://127.0.0.1:8000/numbers/extract/?number=20" -Method POST
```

**Postman:**
- Método: POST
- URL: `http://127.0.0.1:8000/numbers/extract/?number=20`

**Respuesta:**
```json
{
  "message": "Número 20 extraído correctamente"
}
```

#### 2. Número faltante

**GET** `/numbers/missing/`

**Ejemplos:**

```bash
# curl (Linux/Mac)
curl -X GET "http://127.0.0.1:8000/numbers/missing/"

# PowerShell (Windows)
Invoke-RestMethod -Uri "http://127.0.0.1:8000/numbers/missing/" -Method GET
```

**Postman:**
- Método: GET
- URL: `http://127.0.0.1:8000/numbers/missing/`

**Respuesta:**
```json
{
  "missing_number": 20
}
```

#### 3. Reiniciar conjunto

**POST** `/numbers/reset/`

**Ejemplos:**

```bash
# curl (Linux/Mac)
curl -X POST "http://127.0.0.1:8000/numbers/reset/"

# PowerShell (Windows)
Invoke-RestMethod -Uri "http://127.0.0.1:8000/numbers/reset/" -Method POST
```

**Postman:**
- Método: POST
- URL: `http://127.0.0.1:8000/numbers/reset/`

**Respuesta:**
```json
{
  "message": "Conjunto reiniciado correctamente"
}
```

### Pruebas

Ejecutar las pruebas unitarias:

```bash
cd NextTecnology/api_project
pytest -v
```

**Salida esperada:**
```
app/test/test_number.py::test_extract_number PASSED
app/test/test_number.py::test_missing_number PASSED
app/test/test_number.py::test_invalid_number PASSED
app/test/test_number.py::test_reset_allows_new_extraction PASSED
```

### Tecnologías

- **Python 3.13**: Lenguaje principal
- **FastAPI**: Framework web
- **Uvicorn**: Servidor ASGI
- **Pytest**: Framework de pruebas
