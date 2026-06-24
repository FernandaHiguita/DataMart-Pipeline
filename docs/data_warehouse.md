# Online Retail Analytics Data Warehouse

## Overview

The **Online Retail Analytics Data Warehouse** was designed to support business intelligence, reporting, and sales analysis for retail transaction data.

The solution integrates historical and current sales records from multiple sources:

* `data.csv`
* `online_retail_II.xlsx`

These datasets are processed through a layered architecture following modern Data Engineering practices.

```text
Source Files
      │
      ▼
  Bronze Layer
      │
      ▼
  Silver Layer
      │
      ▼
Data Warehouse (Gold Layer)
      │
      ▼
   Power BI
```

The objective is to provide a **single source of truth** for sales performance analysis, customer behavior, product performance, and geographic insights.

---

# Architecture

## Bronze Layer

Stores raw data exactly as received from source systems.

### Tables

```text
bronze.raw_online_retail
bronze.raw_online_retail_ii
```

### Purpose

* Preserve original data
* Enable auditing
* Support reprocessing

---

## Silver Layer

Stores cleaned and standardized datasets.

### Tables

```text
silver.sales_clean
silver.customers_clean
silver.products_clean
silver.countries_clean
```

### Transformations

* Remove duplicates
* Handle missing values
* Standardize column names
* Validate business rules
* Convert data types

---

## Gold Layer (Data Warehouse)

Stores business-ready dimensional models optimized for analytics.

### Schema

```text
dw
```

---

# Data Model

The warehouse follows a **Star Schema** design.

```text
                    dim_date
                        │
                        │
                        ▼

dim_customer ───► fact_sales ◄─── dim_product
                        │
                        │
                        ▼

                   dim_country
```

---

# Fact Table

## fact_sales

The central table containing sales transactions.

### Granularity

One record per product sold within an invoice.

### Example

```text
Invoice 536365
 ├─ Product A
 ├─ Product B
 └─ Product C
```

Results in:

```text
3 rows in fact_sales
```

### Columns

| Column       | Description                  |
| ------------ | ---------------------------- |
| sales_key    | Surrogate primary key        |
| invoice_no   | Invoice identifier           |
| date_key     | Date dimension reference     |
| product_key  | Product dimension reference  |
| customer_key | Customer dimension reference |
| country_key  | Country dimension reference  |
| quantity     | Units sold                   |
| unit_price   | Product price                |
| revenue      | Quantity × Unit Price        |
| load_date    | ETL load timestamp           |

### Measures

* Quantity Sold
* Revenue
* Average Order Value
* Total Sales

---

# Dimensions

## dim_product

Stores product information.

### Attributes

| Column      | Description         |
| ----------- | ------------------- |
| product_key | Surrogate key       |
| stock_code  | Product identifier  |
| description | Product description |

### Business Purpose

* Product performance analysis
* Best-selling products
* Revenue by product

---

## dim_customer

Stores customer information.

### Attributes

| Column       | Description                  |
| ------------ | ---------------------------- |
| customer_key | Surrogate key                |
| customer_id  | Business customer identifier |

### Business Purpose

* Customer segmentation
* Customer lifetime value
* Purchase behavior analysis

---

## dim_country

Stores geographic information.

### Attributes

| Column       | Description      |
| ------------ | ---------------- |
| country_key  | Surrogate key    |
| country_name | Customer country |

### Business Purpose

* Geographic sales analysis
* Market performance
* Regional reporting

---

## dim_date

Stores calendar attributes.

### Attributes

| Column       | Description       |
| ------------ | ----------------- |
| date_key     | YYYYMMDD format   |
| full_date    | Date              |
| day          | Day number        |
| month        | Month number      |
| month_name   | Month name        |
| quarter      | Quarter           |
| year         | Year              |
| week_of_year | Week number       |
| day_name     | Day name          |
| is_weekend   | Weekend indicator |

### Business Purpose

* Time-series analysis
* Monthly reporting
* Seasonal trends
* Year-over-year comparisons

---

# Design Decisions

## Star Schema

A star schema was selected because:

* Simple structure
* Fast analytical queries
* Easy integration with Power BI
* Reduced join complexity

---

## Surrogate Keys

All dimensions use surrogate keys instead of business keys.

### Example

```text
product_key
customer_key
country_key
```

### Benefits

* Improved query performance
* Historical tracking support
* Reduced dependency on source systems

---

## Revenue Storage

Revenue is physically stored in the fact table.

```sql
revenue = quantity * unit_price
```

### Benefits

* Faster reporting
* Reduced calculations in BI tools

---

# Data Quality Rules

The following rules are applied during the Silver Layer processing.

## Duplicate Detection

```text
InvoiceNo + StockCode + InvoiceDate
```

Duplicates are removed.

---

## Quantity Validation

```text
Quantity ≠ 0
```

---

## Price Validation

```text
UnitPrice ≥ 0
```

---

## Revenue Validation

```text
Revenue ≥ 0
```

---

## Customer Validation

```text
CustomerID must be valid when available
```

---

# Indexing Strategy

Indexes were created on frequently queried columns.

```sql
date_key
product_key
customer_key
country_key
invoice_no
```

### Benefits

* Faster filtering
* Improved Power BI performance
* Reduced query execution time

---

# ETL Workflow

```text
1. Extract
   ├─ data.csv
   └─ online_retail_II.xlsx

2. Bronze Load
   ├─ Raw storage
   └─ Audit preservation

3. Silver Processing
   ├─ Cleansing
   ├─ Validation
   ├─ Deduplication
   └─ Standardization

4. Dimension Loading
   ├─ dim_product
   ├─ dim_customer
   ├─ dim_country
   └─ dim_date

5. Fact Loading
   └─ fact_sales

6. Power BI Refresh
```

---

# Business Questions Supported

## Sales Performance

* What are the total sales by month?
* What is the monthly growth rate?
* Which products generate the highest revenue?

## Customer Analysis

* Who are the top customers?
* How many active customers exist?
* What is the average customer spend?

## Product Analysis

* Which products sell the most?
* Which products generate the most revenue?

## Geographic Analysis

* Which countries generate the highest sales?
* Which markets are growing fastest?

## Time Analysis

* Sales by day, month, quarter, and year
* Seasonal purchasing patterns
* Year-over-year comparisons

---

# Technology Stack

| Layer            | Technology      |
| ---------------- | --------------- |
| Orchestration    | Apache Airflow  |
| Processing       | Python (Pandas) |
| Database         | PostgreSQL      |
| Data Warehouse   | Star Schema     |
| Visualization    | Power BI        |
| Version Control  | Git & GitHub    |
| Containerization | Docker          |

---

# Expected Outcomes

The solution provides:

* Centralized analytical repository
* Consistent business metrics
* Improved reporting performance
* Scalable architecture
* Power BI integration
* Foundation for future advanced analytics and machine learning initiatives

This Data Warehouse serves as the analytical layer of the Online Retail Analytics platform and supports decision-making through reliable, structured, and business-ready data.
