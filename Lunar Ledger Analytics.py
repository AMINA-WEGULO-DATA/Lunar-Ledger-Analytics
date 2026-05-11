# Luna Ledger Analytics
# (Personal Finance EDA)
# This notebook explores a personal finance dataset to understand spending patterns,transaction types, category breakdowns, and monthly behavior.

#---INPUTS AND SETUP---
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

sns.set_theme(style="whitegrid")

#---LOAD DATA---
file_path = r"C:\Users\User\Downloads\archive (10)\personal_transactions_dashboard_ready (2).xlsx"
df = pd.read_excel(file_path)
output_dir = Path("output")
output_dir.mkdir(exist_ok=True)

#---INSPECT DATA---

print("DF HEAD")
print(df.head().to_string(index=False))

print("\nDF SHAPE")
print(df.shape)

print("\nDF COLUMNS")
print(df.columns.tolist())

print("\nDF INFO")
df.info()

print("\nMISSING VALUES")
print(df.isnull().sum())

print("\nDUPLICATES")
print(df.duplicated().sum())

print("\nSUMMARY STATS")
print(df.describe(include="all").to_string())

#---CLEAN DATA--- 
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")
df["Transaction Type"] = df["Transaction Type"].str.strip().str.lower()
df["Category"] = df["Category"].str.strip()
df["Description"] = df["Description"].str.strip()
df["Account Name"] = df["Account Name"].str.strip()
df["Month"] = df["Date"].dt.to_period("M").astype(str)
#---ANALYSIS TABLE--
print("\nTRANSACTION TYPE COUNTS")
print(df["Transaction Type"].value_counts().to_string())

print("\nTRANSACTION TYPE TOTALS")
type_totals = df.groupby("Transaction Type")["Amount"].sum().sort_values(ascending=False)
print(type_totals.to_string())

print("\nTOP 10 CATEGORIES BY COUNT")
print(df["Category"].value_counts().head(10).to_string())

print("\nTOP 10 CATEGORIES BY TOTAL AMOUNT")
category_totals = df.groupby("Category")["Amount"].sum().sort_values(ascending=False).head(10)
print(category_totals.to_string())

print("\nMONTHLY TOTALS")
monthly_totals = df.groupby("Month")["Amount"].sum()
print(monthly_totals.to_string())

print("\nTOP 10 DESCRIPTIONS")
top_descriptions = df["Description"].value_counts().head(10)
print(top_descriptions.to_string())
#---CHARTS---
print("\nACCOUNT TOTALS")
account_totals = df.groupby("Account Name")["Amount"].sum().sort_values(ascending=False)
print(account_totals.to_string())
plt.figure(figsize=(7, 4))
sns.barplot(x=type_totals.index, y=type_totals.values, palette="Set2")
plt.title("Total Amount by Transaction Type")
plt.xlabel("Transaction Type")
plt.ylabel("Total Amount")
plt.tight_layout()
plt.savefig(output_dir / "01_transaction_type_totals.png", dpi=300, bbox_inches="tight")
plt.show()

plt.figure(figsize=(10, 5))
sns.barplot(x=category_totals.values, y=category_totals.index, palette="viridis")
plt.title("Top 10 Categories by Total Amount")
plt.xlabel("Total Amount")
plt.ylabel("Category")
plt.tight_layout()
plt.savefig(output_dir / "02_top_categories.png", dpi=300, bbox_inches="tight")
plt.show()

monthly_plot = monthly_totals.copy()
monthly_plot.index = pd.to_datetime(monthly_plot.index)

plt.figure(figsize=(12, 5))
plt.plot(monthly_plot.index, monthly_plot.values, marker="o", linewidth=2)
plt.title("Monthly Total Amount Over Time")
plt.xlabel("Month")
plt.ylabel("Total Amount")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(output_dir / "03_monthly_totals.png", dpi=300, bbox_inches="tight")
plt.show()

plt.figure(figsize=(10, 5))
sns.barplot(x=top_descriptions.values, y=top_descriptions.index, palette="magma")
plt.title("Top 10 Transaction Descriptions")
plt.xlabel("Count")
plt.ylabel("Description")
plt.tight_layout()
plt.savefig(output_dir / "04_top_descriptions.png", dpi=300, bbox_inches="tight")
plt.show()

plt.figure(figsize=(8, 5))
sns.histplot(df["Amount"], bins=30, kde=True, color="steelblue")
plt.title("Distribution of Transaction Amounts")
plt.xlabel("Amount")
plt.ylabel("Frequency")
plt.tight_layout()
plt.savefig(output_dir / "05_amount_distribution.png", dpi=300, bbox_inches="tight")
plt.show()

plt.figure(figsize=(10, 5))
sns.barplot(x=account_totals.values, y=account_totals.index, palette="cubehelix")
plt.title("Total Amount by Account Name")
plt.xlabel("Total Amount")
plt.ylabel("Account Name")
plt.tight_layout()
plt.savefig(output_dir / "06_account_totals.png", dpi=300, bbox_inches="tight")
plt.show()
#---SUMMARY---
summary = pd.DataFrame({
    "metric": [
        "rows",
        "columns",
        "missing_values",
        "duplicate_rows",
        "credit_rows",
        "debit_rows",
        "total_amount"
    ],
    "value": [
        len(df),
        df.shape[1],
        int(df.isnull().sum().sum()),
        int(df.duplicated().sum()),
        int((df["Transaction Type"] == "credit").sum()),
        int((df["Transaction Type"] == "debit").sum()),
        float(df["Amount"].sum())
    ]
})

summary.to_csv(output_dir / "project_summary.csv", index=False)
print("\nPROJECT SUMMARY SAVED")
print(summary.to_string(index=False))