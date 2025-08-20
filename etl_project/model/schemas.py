"""
📌 Definiciones de esquemas y tablas (DDL)
=========================================
"""

RAW_CHARGES_DDL = """
-- Esquema y tabla de staging (entrada)
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

CARGO_DDL = """
-- Tabla final de "Cargo", datos transformados y limpios
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

ALTER_CARGO_AMOUNT = """
-- Ajuste de precisión de columna amount en Cargo
ALTER TABLE public."Cargo"
ALTER COLUMN amount TYPE numeric(20,2);
"""

COMPANIES_AND_CHARGES_DDL = """
-- Tablas de salida para dispersión
CREATE TABLE IF NOT EXISTS public.companies (
  id   varchar(24) PRIMARY KEY,
  name varchar(130) NULL
);

CREATE TABLE IF NOT EXISTS public.charges (
  id          varchar(24) PRIMARY KEY,
  company_id  varchar(24) NOT NULL REFERENCES public.companies(id),
  amount      numeric(20,2) NOT NULL,
  status      varchar(30) NOT NULL,
  created_at  timestamp NOT NULL,
  updated_at  timestamp NULL
);
"""
