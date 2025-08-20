
# ================
# Limpieza (TRUNCATE)
# ================
TRUNCATE_CARGO = 'TRUNCATE TABLE public."Cargo";'

TRUNCATE_TABLES = """
-- Limpieza de las tablas de dispersión
TRUNCATE TABLE public.charges;
TRUNCATE TABLE public.companies CASCADE;
"""

# ===================
# Inserciones en Cargo
# ===================
INSERT_CARGO = """
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

# ===========================
# Inserciones en Companies/Charges
# ===========================
INSERT_COMPANIES = """
INSERT INTO public.companies(id, name)
SELECT DISTINCT company_id, company_name
FROM public."Cargo"
ON CONFLICT (id) DO NOTHING;
"""

INSERT_CHARGES = """
INSERT INTO public.charges(id, company_id, amount, status, created_at, updated_at)
SELECT id, company_id, amount, status, created_at, updated_at
FROM public."Cargo"
ON CONFLICT (id) DO NOTHING;
"""
