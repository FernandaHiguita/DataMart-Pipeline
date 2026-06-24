from pathlib import Path

import pandas as pd


# =====================================================
# CONFIGURATION
# =====================================================

DATA_PATH = Path("data/raw/data.csv")


# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv(
    DATA_PATH,
    encoding="latin1"
)

print("\n" + "=" * 60)
print("DATASET OVERVIEW")
print("=" * 60)

print(f"Rows: {df.shape[0]:,}")
print(f"Columns: {df.shape[1]}")


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

print(df.describe().T)


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
# BUSINESS RULES CHECK
# =====================================================

print("\nBUSINESS VALIDATION")
print("-" * 60)

negative_quantity = (
    df["Quantity"] < 0
).sum()

negative_price = (
    df["UnitPrice"] < 0
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
# REVENUE
# =====================================================

df["Revenue"] = (
    df["Quantity"] *
    df["UnitPrice"]
)

print("\nREVENUE")
print("-" * 60)

print(
    df["Revenue"]
    .describe()
)