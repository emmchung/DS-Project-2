
# Finalizes the cleaned Virginia CDC FluView dataset by removing columns
# that are unnecessary for time-series modeling.
# This script should be run after the first preprocessing script (clean_data.py).
#
# Input: Data/VirginiaFlu_cleaned.csv (output from first preprocessing script)
# Output: Data/VirginiaFlu.csv (final dataset for SARIMA modeling)
# Required library: pandas
# Run from the repository root: python 02_Preprocessing2.py

import pandas as pd

# Define input and output file locations
Input = "Data/VirginiaFlu_cleaned.csv"
Output = "Data/VirginiaFlu.csv"

# Load the cleaned dataset from the first preprocessing script
df = pd.read_csv(Input)

# Remove redundant region identifiers and the intermediate season_start variable
# while retaining the variables needed for modeling
columns_to_remove = ["region_type", "region", "season_start"]

df = df.drop(columns=columns_to_remove)

# Save the final preprocessed dataset for SARIMA modeling
df.to_csv(Output, index=False)

# Confirm successful completion
print("Final data cleaning completed successfully!")
