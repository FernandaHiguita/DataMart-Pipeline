-- =====================================================
-- DATA WAREHOUSE RETAIL SALES
-- Proyecto: Online Retail Analytics
-- Autor: Fernanda Higuita
-- =====================================================

-- =====================================================
-- CREAR ESQUEMA
-- =====================================================

CREATE SCHEMA IF NOT EXISTS dw;

-- =====================================================
-- DIMENSION PRODUCTO
-- =====================================================

CREATE TABLE IF NOT EXISTS dw.dim_product (

    product_key BIGSERIAL PRIMARY KEY,

    stock_code VARCHAR(50) NOT NULL,

    description VARCHAR(500),

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_dim_product_stock_code
        UNIQUE (stock_code)

);

COMMENT ON TABLE dw.dim_product IS 'Dimensión de productos';

-- =====================================================
-- DIMENSION CLIENTE
-- =====================================================

CREATE TABLE IF NOT EXISTS dw.dim_customer (

    customer_key BIGSERIAL PRIMARY KEY,

    customer_id VARCHAR(50),

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_dim_customer_customer_id
        UNIQUE (customer_id)

);

COMMENT ON TABLE dw.dim_customer IS 'Dimensión de clientes';

-- =====================================================
-- DIMENSION PAIS
-- =====================================================

CREATE TABLE IF NOT EXISTS dw.dim_country (

    country_key BIGSERIAL PRIMARY KEY,

    country_name VARCHAR(100) NOT NULL,

    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_dim_country_name
        UNIQUE (country_name)

);

COMMENT ON TABLE dw.dim_country IS 'Dimensión geográfica';

-- =====================================================
-- DIMENSION FECHA
-- =====================================================

CREATE TABLE IF NOT EXISTS dw.dim_date (

    date_key INTEGER PRIMARY KEY,

    full_date DATE NOT NULL,

    day INTEGER NOT NULL,

    month INTEGER NOT NULL,

    month_name VARCHAR(20) NOT NULL,

    quarter INTEGER NOT NULL,

    year INTEGER NOT NULL,

    week_of_year INTEGER NOT NULL,

    day_name VARCHAR(20) NOT NULL,

    is_weekend BOOLEAN NOT NULL

);

COMMENT ON TABLE dw.dim_date IS 'Dimensión calendario';

-- =====================================================
-- TABLA DE HECHOS
-- =====================================================

CREATE TABLE IF NOT EXISTS dw.fact_sales (

    sales_key BIGSERIAL PRIMARY KEY,

    invoice_no VARCHAR(50) NOT NULL,

    date_key INTEGER NOT NULL,

    product_key BIGINT NOT NULL,

    customer_key BIGINT,

    country_key BIGINT NOT NULL,

    quantity INTEGER NOT NULL,

    unit_price NUMERIC(12,2) NOT NULL,

    revenue NUMERIC(14,2) NOT NULL,

    load_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_fact_sales_date
        FOREIGN KEY (date_key)
        REFERENCES dw.dim_date(date_key),

    CONSTRAINT fk_fact_sales_product
        FOREIGN KEY (product_key)
        REFERENCES dw.dim_product(product_key),

    CONSTRAINT fk_fact_sales_customer
        FOREIGN KEY (customer_key)
        REFERENCES dw.dim_customer(customer_key),

    CONSTRAINT fk_fact_sales_country
        FOREIGN KEY (country_key)
        REFERENCES dw.dim_country(country_key)

);

COMMENT ON TABLE dw.fact_sales IS 'Tabla de hechos de ventas';

-- =====================================================
-- INDICES PARA CONSULTAS ANALITICAS
-- =====================================================

CREATE INDEX IF NOT EXISTS idx_fact_sales_date
ON dw.fact_sales(date_key);

CREATE INDEX IF NOT EXISTS idx_fact_sales_product
ON dw.fact_sales(product_key);

CREATE INDEX IF NOT EXISTS idx_fact_sales_customer
ON dw.fact_sales(customer_key);

CREATE INDEX IF NOT EXISTS idx_fact_sales_country
ON dw.fact_sales(country_key);

CREATE INDEX IF NOT EXISTS idx_fact_sales_invoice
ON dw.fact_sales(invoice_no);

-- =====================================================
-- VALIDACIONES
-- =====================================================

ALTER TABLE dw.fact_sales
ADD CONSTRAINT chk_quantity_positive
CHECK (quantity <> 0);

ALTER TABLE dw.fact_sales
ADD CONSTRAINT chk_unit_price_positive
CHECK (unit_price >= 0);

ALTER TABLE dw.fact_sales
ADD CONSTRAINT chk_revenue_positive
CHECK (revenue >= 0);

-- =====================================================
-- FIN SCRIPT
-- =====================================================