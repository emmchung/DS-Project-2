
# Cleans and organizes CDC FluView data for Virginia by validating observations,
# removing duplicates, and creating chronological variables for time-series modeling.
# Retains influenza seasons 2016-17 through 2025-26.
#
# Input: Data/ICL_NREVSS_Clinical_Labs.csv (original CDC FluView data)
# Output: Data/VirginiaFlu_cleaned.csv (cleaned dataset)
# Required libraries: pandas, numpy
# Run from the repository root: python clean_data.py

import pandas as pd
import numpy as np
from pathlib import Path


# Define the location of the original CDC dataset
Input = "Data/ICL_NREVSS_Clinical_Labs.csv"

# Load data, skipping the first explanatory line
df = pd.read_csv(Input, skiprows=1)

# Standardize column names
df.columns = (df.columns.str.strip().str.lower().str.replace(" ", "_"))

# Verify that all observations are from Virginia
if not df["region"].astype(str).str.strip().eq("Virginia").all():
    raise ValueError("Dataset contains observations outside Virginia.")

# Convert relevant columns to numeric values and check for missing data
numeric_cols = ["year", "week", "total_specimens", "total_a", "total_b", "percent_positive", "percent_a", "percent_b"]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

print("Missing values:")
print(df.isna().sum())

if df[numeric_cols].isna().any().any():
    raise ValueError("Missing or invalid numeric data detected.")

# Remove duplicate rows and check for conflicting year-week observations
df = df.drop_duplicates()

if df.duplicated(["year", "week"]).any():
    raise ValueError("Conflicting observations for the same week.")

# Validate specimen counts and positivity percentages
if (df[["total_specimens", "total_a", "total_b"]] < 0).any().any():
    raise ValueError("Negative specimen counts detected.")

if (df["total_a"] + df["total_b"] > df["total_specimens"]).any():
    raise ValueError("Positive tests exceed total specimens.")

for col in ["percent_positive", "percent_a", "percent_b"]:
    if not df[col].between(0, 100).all():
        raise ValueError(f"Invalid values found in {col}")

# Assign influenza seasons beginning in week 40 and retain 2016-17 through 2025-26
df["season_start"] = np.where(
    df["week"] >= 40,
    df["year"],
    df["year"] - 1
)

df = df[df["season_start"].between(2016, 2025)].copy()

# Create a label for each influenza season
df["season"] = (
    df["season_start"].astype(str)
    + "-"
    + (df["season_start"] + 1).astype(str)
)

# Convert CDC epidemiological year-week values to Sunday start dates
# using the week containing January 4 as week 1
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

# Sort observations chronologically and verify that no weeks are missing
df = df.sort_values("week_start").reset_index(drop=True)

weekly_difference = df["week_start"].diff().dropna()

if not weekly_difference.eq(pd.Timedelta(days=7)).all():
    raise ValueError("Missing weeks detected in the dataset.")

# Create a unique year-week identifier for each observation
df["year_week"] = (
    df["year"].astype(int).astype(str)
    + "-W"
    + df["week"].astype(int).astype(str).str.zfill(2)
)

# Create a continuous week index across the dataset
df["week_index"] = np.arange(1, len(df) + 1)

# Number the weeks within each influenza season
df["season_week"] = df.groupby("season").cumcount() + 1

# Save the cleaned dataset for the second preprocessing script
df.to_csv("Data/VirginiaFlu_cleaned.csv", index=False)

print("Data cleaning completed successfully!")
print("File saved to: Data/VirginiaFlu_cleaned.csv")
