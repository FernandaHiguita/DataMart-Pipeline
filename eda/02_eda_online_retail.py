from pathlib import Path

import pandas as pd


# =====================================================
# CONFIGURATION
# =====================================================

DATA_PATH = Path("data/raw/online_retail_II.xlsx")


# =====================================================
# LOAD DATA
# =====================================================

sheet_2009 = pd.read_excel(
    DATA_PATH,
    sheet_name="Year 2009-2010"
)

sheet_2010 = pd.read_excel(
    DATA_PATH,
    sheet_name="Year 2010-2011"
)

df = pd.concat(
    [sheet_2009, sheet_2010],
    ignore_index=True
)

print("\n" + "=" * 60)
print("DATASET OVERVIEW")
print("=" * 60)

print(f"Rows: {df.shape[0]:,}")
print(f"Columns: {df.shape[1]}")


# =====================================================
# SHEETS INFORMATION
# =====================================================

print("\nWORKSHEETS")
print("-" * 60)

print(f"2009-2010 Rows: {sheet_2009.shape[0]:,}")
print(f"2010-2011 Rows: {sheet_2010.shape[0]:,}")

print(
    f"Total Rows: "
    f"{sheet_2009.shape[0] + sheet_2010.shape[0]:,}"
)


# =====================================================
# COLUMNS
# =====================================================

print("\nCOLUMNS")
print("-" * 60)

for col in df.columns:
    print(col)


# =====================================================
# PREVIEW
# =====================================================

print("\nPREVIEW")
print("-" * 60)

print(df.head())


# =====================================================
# STRUCTURE
# =====================================================

print("\nSTRUCTURE")
print("-" * 60)

print(df.info())

print("\nDATA TYPES")
print(df.dtypes)


# =====================================================
# MISSING VALUES
# =====================================================

print("\nMISSING VALUES")
print("-" * 60)

missing = pd.DataFrame({
    "null_count": df.isnull().sum(),
    "null_pct": (
        df.isnull()
        .mean()
        .mul(100)
        .round(2)
    )
})

print(
    missing.sort_values(
        "null_pct",
        ascending=False
    )
)


# =====================================================
# DUPLICATES
# =====================================================

print("\nDUPLICATES")
print("-" * 60)

print(
    f"Duplicate rows: "
    f"{df.duplicated().sum():,}"
)


# =====================================================
# CARDINALITY
# =====================================================

print("\nCARDINALITY")
print("-" * 60)

cardinality = pd.DataFrame({
    "column": df.columns,
    "unique_values": [
        df[col].nunique()
        for col in df.columns
    ]
})

print(
    cardinality.sort_values(
        by="unique_values",
        ascending=False
    )
)


# =====================================================
# NUMERICAL ANALYSIS
# =====================================================

print("\nNUMERICAL VARIABLES")
print("-" * 60)

print(
    df.describe(
        include="all"
    ).T
)


# =====================================================
# CATEGORICAL ANALYSIS
# =====================================================

print("\nCATEGORICAL VARIABLES")
print("-" * 60)

categorical_columns = (
    df.select_dtypes(
        include=["object"]
    )
    .columns
)

for col in categorical_columns:
    print(
        f"\n{col}: "
        f"{df[col].nunique()} unique values"
    )


# =====================================================
# BUSINESS VALIDATION
# =====================================================

print("\nBUSINESS VALIDATION")
print("-" * 60)

negative_quantity = (
    df["Quantity"] < 0
).sum()

negative_price = (
    df["Price"] < 0
).sum()

print(
    f"Negative quantities: "
    f"{negative_quantity:,}"
)

print(
    f"Negative prices: "
    f"{negative_price:,}"
)


# =====================================================
# DATE CONVERSION CHECK
# =====================================================

print("\nDATE VALIDATION")
print("-" * 60)

df["InvoiceDate"] = pd.to_datetime(
    df["InvoiceDate"],
    errors="coerce"
)

print(
    f"Invalid dates: "
    f"{df['InvoiceDate'].isnull().sum():,}"
)


# =====================================================
# REVENUE
# =====================================================

df["Revenue"] = (
    df["Quantity"] *
    df["Price"]
)

print("\nREVENUE")
print("-" * 60)

print(
    df["Revenue"]
    .describe()
)