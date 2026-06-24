# Dataset: data.csv

## Business Context

This dataset contains retail sales transactions, including invoice information, products, quantities sold, prices, customers, and countries. It represents the operational sales activity of a retail business and serves as a source for analytical reporting and business intelligence.

---

# Dataset Overview

## Shape

| Metric  | Value   |
| ------- | ------- |
| Rows    | 541,909 |
| Columns | 8       |

## Columns

* InvoiceNo
* StockCode
* Description
* Quantity
* InvoiceDate
* UnitPrice
* CustomerID
* Country

### Interpretation

The dataset contains a large volume of transactional records with a compact structure focused on sales operations. The available attributes allow the identification of products, customers, locations, and transaction metrics, making it suitable for dimensional modeling and sales analytics.

---

# Preliminary View

### Interpretation

The dataset is stored at the transaction line level. Each record represents a product included within a sales invoice. A single invoice may contain multiple products, resulting in multiple records sharing the same InvoiceNo.

Main business entities identified:

* Invoice
* Product
* Customer
* Date
* Country

---

# Data Structure

| Column      | Type    |
| ----------- | ------- |
| InvoiceNo   | str     |
| StockCode   | str     |
| Description | str     |
| Quantity    | int64   |
| InvoiceDate | str     |
| UnitPrice   | float64 |
| CustomerID  | float64 |
| Country     | str     |

### Interpretation

The dataset combines categorical, numerical, and transactional attributes. InvoiceDate is currently stored as a string and should be converted to datetime during transformation. CustomerID is stored as float due to the presence of null values.

---

# Data Quality

## Missing Values

| Column            | Null Values |
| ----------------- | ----------- |
| CustomerID        | 135,080     |
| Description       | 1,454       |
| Remaining Columns | 0           |

### Interpretation

Most columns have complete information. Missing values are concentrated in CustomerID, suggesting that a significant number of transactions are not associated with registered customers. Description contains a small number of missing values that should be reviewed during data cleansing.

---

## Duplicates

| Metric         | Value |
| -------------- | ----- |
| Duplicate Rows | 5,268 |

### Interpretation

The dataset contains duplicated records that should be evaluated and potentially removed during the Silver transformation stage to prevent inconsistencies in analytical calculations.

---

# Cardinality Analysis

| Column      | Unique Values |
| ----------- | ------------- |
| InvoiceNo   | 25,900        |
| InvoiceDate | 23,260        |
| StockCode   | 4,070         |
| Description | 4,223         |
| CustomerID  | 4,372         |
| UnitPrice   | 1,630         |
| Quantity    | 722           |
| Country     | 38            |

### Interpretation

The relatively low number of countries and customers compared to transaction volume suggests strong dimensional candidates. InvoiceNo and InvoiceDate indicate a high level of transactional detail suitable for analytical reporting.

---

# Candidate Dimensions

## Dim Product

* StockCode
* Description

## Dim Customer

* CustomerID

## Dim Country

* Country

## Dim Date

Derived from InvoiceDate.

---

# Candidate Fact Table

## Fact Sales

### Measures

* Quantity
* UnitPrice

### Derived Metrics

* Revenue = Quantity × UnitPrice

---

# Candidate Silver Rules

* Convert InvoiceDate to datetime.
* Remove duplicated records.
* Handle null CustomerID values.
* Review and clean null Description values.
* Validate negative quantities (returns).
* Validate negative prices.
* Create Revenue metric.
* Standardize country values.

---

# Lakehouse Role

## Bronze

Raw transactional sales data.

## Silver

Data cleansing, standardization, and quality validation.

## Gold

Sales analytics, KPIs, customer behavior analysis, and Power BI reporting.

---

# Conclusion

The dataset contains detailed retail transaction data with sufficient granularity to serve as the primary sales fact source in the analytical model. After applying quality validations and business rules, it can be transformed into a fact table supported by Product, Customer, Country, and Date dimensions. The dataset is suitable for loading into Supabase and subsequent visualization in Power BI.
