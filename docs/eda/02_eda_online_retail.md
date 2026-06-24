# Dataset: online_retail_II.xlsx

## Business Context

Historical retail sales dataset containing transaction records from 2009 to 2011. The dataset stores invoice information, products sold, quantities, prices, customer identifiers, and countries.

It represents the historical transactional source used for sales analysis, customer behavior analysis, and revenue reporting.

---

# Dataset Overview

## Source Structure

The file contains two worksheets:

* Year 2009-2010
* Year 2010-2011

Both worksheets share the same schema and can be consolidated into a single transactional dataset during ingestion.

## Columns

* Invoice
* StockCode
* Description
* Quantity
* InvoiceDate
* Price
* Customer ID
* Country

### Interpretation

The dataset stores transactional retail sales data at the invoice line level. Each record represents a product sold within a specific invoice transaction.

---

# Preliminary Findings

Main business entities identified:

* Invoice
* Product
* Customer
* Date
* Country

The structure is highly similar to the previously analyzed dataset and is suitable for dimensional modeling.

---

# Data Structure

| Column      | Business Meaning    |
| ----------- | ------------------- |
| Invoice     | Invoice identifier  |
| StockCode   | Product identifier  |
| Description | Product description |
| Quantity    | Units sold          |
| InvoiceDate | Transaction date    |
| Price       | Unit price          |
| Customer ID | Customer identifier |
| Country     | Customer country    |

### Observations

* InvoiceDate should be converted to datetime.
* Customer ID may contain null values.
* Product and invoice identifiers should be treated as business keys.
* Price and Quantity are candidate measures.

---

# Candidate Dimensions

## Dim Product

* StockCode
* Description

## Dim Customer

* Customer ID

## Dim Country

* Country

## Dim Date

Derived from InvoiceDate.

---

# Candidate Fact Table

## Fact Sales

Measures:

* Quantity
* Price

Derived Metrics:

* Revenue = Quantity × Price

---

# Candidate Silver Rules

* Merge both worksheets into a single dataset.
* Convert InvoiceDate to datetime.
* Remove duplicate records.
* Validate null Customer ID values.
* Validate null Description values.
* Standardize country values.
* Create Revenue metric.
* Validate negative quantities and prices.

---

# Lakehouse Role

## Bronze

Raw historical transactional data.

## Silver

Data quality validation and standardization.

## Gold

Sales analytics and historical KPI generation.

---

# Conclusion

The dataset contains historical retail transaction data covering two fiscal periods. Its structure is consistent with transactional sales systems and can be integrated into the analytical model as a sales fact source supported by Product, Customer, Country, and Date dimensions.
