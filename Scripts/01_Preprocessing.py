### THINGS IN THIS FILE NEED TO BE DELETED PERTAINING TO "FILEPATH" 
# Cleans and organizes the CDC data for Virginia by validating observations, removing duplicates, and creating chronological variables.

import pandas as pd
import numpy as np
from pathlib import Path

# File locations - DELETE this
#Filepath = Path(r"C:\Users\bryso\PycharmProjects\PythonProject\Stat 2120\Raw Data")
#Input = Filepath / "ICL_NREVSS_Clinical_Labs.csv"

# File location - GENERAL
Input = "Data/ICL_NREVSS_Clinical_Labs.csv"

# Load data (CDC file has an explanatory first line)
df = pd.read_csv(Input, skiprows=1)

# Standardize column names
df.columns = (df.columns.str.strip().str.lower().str.replace(" ", "_"))

# Verify Virginia data
if not df["region"].astype(str).str.strip().eq("Virginia").all():
    raise ValueError("Dataset contains observations outside Virginia.")

# Convert columns to numeric
numeric_cols = ["year", "week", "total_specimens", "total_a", "total_b", "percent_positive", "percent_a", "percent_b"]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Check missing values
print("Missing values:")
print(df.isna().sum())

if df[numeric_cols].isna().any().any():
    raise ValueError("Missing or invalid numeric data detected.")

# Remove duplicate rows
df = df.drop_duplicates()

# Check duplicate year-week combinations
if df.duplicated(["year", "week"]).any():
    raise ValueError("Conflicting observations for the same week.")

# Check invalid values
if (df[["total_specimens", "total_a", "total_b"]] < 0).any().any():
    raise ValueError("Negative specimen counts detected.")

if (df["total_a"] + df["total_b"] > df["total_specimens"]).any():
    raise ValueError("Positive tests exceed total specimens.")

for col in ["percent_positive", "percent_a", "percent_b"]:
    if not df[col].between(0, 100).all():
        raise ValueError(f"Invalid values found in {col}")

# Identify influenza seasons
# Flu seasons begin during week 40
df["season_start"] = np.where(
    df["week"] >= 40,
    df["year"],
    df["year"] - 1
)

# Keep 2021-22 through 2025-26
df = df[df["season_start"].between(2021, 2025)].copy()

df["season"] = (
    df["season_start"].astype(str)
    + "-"
    + (df["season_start"] + 1).astype(str)
)

# Convert CDC epidemiological weeks to Sunday dates
def cdc_week_start(year, week):
    year = int(year)
    week = int(week)

    jan4 = pd.Timestamp(year, 1, 4)
    first_sunday = jan4 - pd.Timedelta(days=(jan4.weekday() + 1) % 7)

    next_jan4 = pd.Timestamp(year + 1, 1, 4)
    next_sunday = next_jan4 - pd.Timedelta(days=(next_jan4.weekday() + 1) % 7)

    date = first_sunday + pd.Timedelta(weeks=week - 1)

    if week < 1 or date >= next_sunday:
        raise ValueError(f"Invalid CDC week: {year}-W{week}")

    return date

df["week_start"] = [cdc_week_start(y, w) for y, w in zip(df["year"], df["week"])]

# Sort observations chronologically
df = df.sort_values("week_start").reset_index(drop=True)

# Check for missing weeks
weekly_difference = df["week_start"].diff().dropna()

if not weekly_difference.eq(pd.Timedelta(days=7)).all():
    raise ValueError("Missing weeks detected in the dataset.")

# Create unique chronological week identifier
df["year_week"] = (
    df["year"].astype(int).astype(str)
    + "-W"
    + df["week"].astype(int).astype(str).str.zfill(2)
)

# Continuous week index
df["week_index"] = np.arange(1, len(df) + 1)

# Week within each influenza season
df["season_week"] = df.groupby("season").cumcount() + 1

DELETE THIS
# Save cleaned dataset containing every week
#df.to_csv(Filepath / "VirginiaFlu_cleaned.csv", index=False)
# Verify that it ran
#print("Data cleaning completed successfully!")
#print("Files saved to:", Filepath)

df.to_csv("Data/VirginiaFlu_cleaned.csv", index=False)
print("Data cleaning completed successfully!")
print("File saved to: Data/VirginiaFlu_cleaned.csv")
