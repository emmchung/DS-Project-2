# README File for Data Establishment 
## Summary
This dataset contains weekly influenza surveillance data for Virginia, obtained from the Centers for Disease Control and Prevention (CDC) through its FluView Interactive Dashboard. The dataset covers five influenza seasons, from 2021-2022 through 2025-2026, and contains information on influenza testing and positivity reported by clinical laboratories. The dataset includes the total number of influenza specimens tested each week, the number of positive tests for influenza A and influenza B, and the corresponding percentages of positive tests. Each observation represents one week of surveillance data (labeled weeks 1-52), allowing us to examine changes in influenza activity over time and compare patterns across seasons. The data were downloaded directly from the CDC FluView dashboard by selecting Virginia as the geographic region and filtering for the five specified influenza seasons. We did some minor preprocessing to prepare the dataset for time series analysis, including removing redundant geographic variables, standardizing column names, and adding a chronological variable to identify and order observations by week number. The cleaned dataset will be stored in our shared GitHub repository (VirginiaFlu.csv) while the original data remain accessible through the CDC FluView dashboard. 
## Provenance
The dataset was obtained directly from the CDC FluView interactive Dashboard by filtering for Virginia and the 2021-2022 through 2025-2026 influenza seasons (FluView). After downloading the CSV file, we removed redundant geographic identifiers (Region type, region), standardized the variable names, and created additional time-related variables to support chronological indexing and seasonal comparisons. The original influenza testing counts and positive values were retained without modification. The cleaned dataset will be stored in our shared GitHub repository as VirginiaFlu.csv, with steps for downloading the original dataset and preprocessing documented for reproducibility.
## License
The dataset is publicly available through the Centers for Disease Control and Prevention (CDC). As a U.S. federal government resource, CDC-produced data are generally considered public domain and may be reused and redistributed with appropriate attribution. The CDC is credited as the original data source, and the dataset is available free of charge through the FluView interactive dashboard. Our use of the data does not imply endorsement by the CDC. 
## Ethical Statement 
The CDC FluView dataset contains publicly available, aggregated influenza surveillance data without personally identifiable information. However, differences in laboratory participation, testing practices, and specimen selection may introduce biases across seasons. We will acknowledge these limitations and avoid interpreting changes in reported influenza positivity rates as direct measures of changes in influenza prevalence.
## Data Dictionary
Variable
Data Type
Description
Considerations
year
Integer
Calendar year of observation
Represent CDC epidemiological weeks rather than standard calendar dates. Influenza seasons span two calendar years. 
week
Integer
Epidemiological week number.
A chronological identifier is necessary to distinguish different weeks from different seasons. 
total_specimens
Integer
Total influenza specimens tested
Reflects specimens submitted and tested by participating laboratories, not all influenza infections in Virginia. Testing volume varies over time. 
total_a
Integer
Number of specimens positive for influenza A.
Counts influenced by testing volume and practices. 
total_b
Integer
Number of specimens positive for influenza B.
Counts influenced by testing volume and practices. 
percent_positive
Float
Percentage of specimens positive for influenza A or B
Rates may be affected by differences in testing practices and specimen selection.
percent_a
Float
Percentage of specimens positive for influenza A.
Rates may be affected by differences in testing practices and specimen selection.
percent_b
Float
Percentage of specimens positive for influenza B.
Rates may be affected by differences in testing practices and specimen selection.
season
string
Influenza season (e.g. 2021-2022)
Derived from year and week. Assumes influenza seasons begin at week 40. 
week_start
String (date format)
Starting date of each epidemiological week (e.g. 10/3/2021)
Accuracy depends on correctly converting CDC week numbering to calendar dates. 
year_week
string
Chronological year-week identifier (e.g. 2022-W01)
Must follow consistent formatting.
week_index
Integer 
Sequential index of weeks across the entire dataset
Assumes observations are correctly ordered. Missing weeks could impact interpretation. 
season_week
Integer 
Sequential week number within each influenza season. 
Assumes consistent season boundaries, accounts for potential 53-week years. 

## Exploratory Plots
<img width="708" height="291" alt="Screenshot 2026-10-14 at 2 13 31 PM" src="https://github.com/user-attachments/assets/7503dc53-e4f1-4e88-b67b-02d2d2f5f295" />
<img width="690" height="279" alt="Screenshot 2026-10-14 at 2 13 12 PM" src="https://github.com/user-attachments/assets/e4976c54-33e6-4a7d-8c66-70f4087d7187" />

