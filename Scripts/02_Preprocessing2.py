# EDITS STILL TO BE MADE HERE
# Removes unnecessary columns from the cleaned Virginia CDC dataset and saves the final version.

import pandas as pd
#from pathlib import Path

# File locations
#Filepath = Path(r"C:\Users\bryso\PycharmProjects\PythonProject\Stat 2120\Raw Data")

Input = "Data/VirginiaFlu_cleaned.csv"
Output = "Data/VirginiaFlu.csv"

#Input = Filepath / "VirginiaFlu_cleaned.csv"
#Output = Filepath / "VirginiaFlu.csv"

# Load cleaned dataset
df = pd.read_csv(Input)

# Remove unnecessary columns
columns_to_remove = ["region_type", "region", "season_start"]

df = df.drop(columns=columns_to_remove)

# Save updated dataset
df.to_csv(Output, index=False)

# Verify that it ran
print("Final data cleaning completed successfully!")
