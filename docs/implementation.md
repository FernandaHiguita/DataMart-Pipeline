# Plan de Implementación — Prueba Técnica DataMart

## Objetivo

Construir una plataforma de datos funcional de extremo a extremo que permita:

* Consumir dos datasets de Kaggle.
* Realizar exploración y validación de calidad.
* Transformar y unificar la información.
* Cargar los datos en PostgreSQL analítico.
* Orquestar todo mediante Apache Airflow.
* Exponer los datos para análisis posterior en Power BI.

---

# Arquitectura Objetivo

```text
GitHub
   |
   v

Docker Compose
   |
   +------------------------------+
   |                              |
   v                              v

PostgreSQL Metadata        PostgreSQL Analytics
(Airflow)                  (DataMart DW)

   ^
   |
   |

Apache Airflow
(Webserver + Scheduler)

   |
   v

DAG Datamart Pipeline

   |
   +-------------------+
   |                   |
   v                   v

Ecommerce Dataset   Historical Dataset
(Kaggle)            (Kaggle)

   |
   v

Transformación

   |
   v

Validación Calidad

   |
   v

Carga DW

   |
   v

Power BI (opcional)
```

---

# Fase 1 — Estructura del Proyecto

```text
datamart-pipeline/
│
├── dags/
│   └── datamart_pipeline.py
│
├── src/
│   ├── extract/
│   ├── transform/
│   ├── load/
│   ├── quality/
│   └── utils/
│
├── sql/
│   ├── ddl.sql
│   └── seeds.sql
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── rejected/
│
├── eda/
│   ├── 01_sales_dataset.ipynb
│   └── 02_historical_dataset.ipynb
│
├── docker/
│
├── docs/
│   ├── decisions.md
│   ├── queries.sql
│   └── architecture.png
│
├── .env.example
├── docker-compose.yml
└── README.md
```

---

# Fase 2 — Docker Compose

Servicios requeridos:

## PostgreSQL Metadata

Base utilizada exclusivamente por Airflow.

```text
DB: airflow
```

---

## PostgreSQL Analytics

Repositorio analítico destino.

```text
DB: datamart_dw
```

---

## Airflow Init

Responsable de:

* Crear usuario administrador.
* Ejecutar migraciones.
* Crear Connections.
* Crear Variables.

---

## Airflow Scheduler

Ejecución automática del DAG.

---

## Airflow Webserver

Disponible en:

```text
http://localhost:8080
```

---

# Fase 3 — Airflow Connections

Crear automáticamente durante el arranque.

## analytics_db

```text
Conn Type: Postgres
Host: postgres_analytics
Database: datamart_dw
```

---

# Fase 4 — Airflow Variables

Inicializar automáticamente.

## sales_file_path

```text
/data/raw/data.csv
```

---

## historical_file_path

```text
/data/raw/online_retail_II.csv
```

---

## load_mode

```text
full
```

---

# Fase 5 — EDA

## Dataset 1

Analizar:

* Shape
* Tipos de datos
* Nulos
* Duplicados
* Revenue
* Cantidades negativas
* Precios inválidos
* CustomerID faltantes

---

## Dataset 2

Analizar:

* Shape
* Tipos de datos
* Nulos
* Fechas
* Solapamientos
* Duplicados
* Compatibilidad estructural

---

## Entregable EDA

Generar:

```text
eda/
├── 01_sales_dataset.ipynb
└── 02_historical_dataset.ipynb
```

---

# Fase 6 — Modelo Analítico

## Dim Products

```text
product_code
product_name
category
```

---

## Dim Customers

```text
customer_id
customer_type
```

customer_type:

```text
identified
anonymous
```

---

## Fact Sales

```text
sale_id
date
country
product_code
customer_id

quantity
unit_price

gross_revenue
net_revenue

transaction_type
```

---

## Rejected Records

```text
record_id
source
reason
created_at
```

---

# Fase 7 — Reglas de Negocio

## Devoluciones

```text
Quantity <= 0
```

Registrar como:

```text
RETURN
```

---

## Ventas válidas

```text
Quantity > 0
AND
UnitPrice > 0
```

---

## Registros rechazados

```text
UnitPrice <= 0
```

Guardar en:

```text
rejected_records
```

---

## Product Codes

Normalizar:

```text
UPPER()
TRIM()
```

---

## Fechas

Convertir a UTC.

---

## Revenue Bruto

```text
quantity * unit_price
```

---

## Revenue Neto

```text
ventas - devoluciones
```

---

# Fase 8 — Manejo de Ambigüedades

## CustomerID nulo

Decisión:

```text
Mantener registro
```

Asignar:

```text
customer_id = UNKNOWN
```

---

## Variaciones de descripción

Elegir:

```text
Descripción más frecuente por código
```

---

## Duplicados entre fuentes

Clave compuesta:

```text
invoice_no
product_code
invoice_date
quantity
unit_price
customer_id
```

---

# Fase 9 — DAG

## Task 1

```text
extract_sales_dataset
```

---

## Task 2

```text
extract_historical_dataset
```

---

## Task 3

```text
transform_data
```

---

## Task 4

```text
quality_validation
```

---

## Task 5

```text
load_datawarehouse
```

---

# Fase 10 — Idempotencia

Antes de cargar:

```sql
DELETE
WHERE load_date = execution_date;
```

o

```sql
UPSERT
```

mediante:

```sql
ON CONFLICT
```

---

# Fase 11 — Power BI

Conectar a:

```text
localhost:5433
```

Base:

```text
datamart_dw
```

---

# Fase 12 — Documentación

## README

Debe explicar:

* Clonar repositorio.
* Configurar .env.
* Levantar Docker.
* Verificar Airflow.
* Ejecutar DAG.
* Consultar PostgreSQL.

---

## decisions.md

Explicar:

* Modelo de datos.
* Manejo de nulos.
* Duplicados.
* Descripciones inconsistentes.
* Idempotencia.

---

## queries.sql

Una consulta por cada pregunta de negocio.

```
```
