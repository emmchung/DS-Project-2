# DS-Project-2
## Contents
This repository contains the code, data, documentation, and results for our analysis and forecasting of seasonal influenza activity in Virginia. The project uses CDC FluView clinical laboratory data and Seasonal Autoregressive Integrated Moving Average (SARIMA) modeling to forecast weekly influenza positivity rates and predict the timing and magnitude of seasonal influenza peaks.

The repository includes:
- The original and preprocessed CDC FluView datasets for Virginia
- Python scripts for data preprocessing, SARIMA model development, and evaluation
- Documentation describing the dataset, preprocessing steps, and modeling approach
- Model outputs, including forecast visualizations, performance metrics, seasonal peak predictions, and summary results
- References and project documentation needed to understand and reproduce the analysis

The analysis uses historical influenza data from the 2016–17 through 2023–24 seasons to develop and select a SARIMA forecasting model. The model is then evaluated on the 2024–25 and 2025–26 seasons by comparing predicted and observed weekly influenza positivity rates and seasonal peak timing. Forecast performance is assessed using mean absolute error (MAE), root mean squared error (RMSE), and peak prediction errors, with results compared against a seasonal-naïve baseline.

## Software and Platform Selection
### Software Types Used
- Visual Studio Code (VS Code)
- Python 3.13
- Git/GitHub
- Windows 11 / macOS 26.2
### Add-on packages
- pandas 3.0.3
- numpy 2.4.6
- matplotlib 3.11.2
- statsmodels 0.15.0
- warnings 
- pathlib
### Platforms used
Visual Studio Code (VS Code) with Python 3.13 and the VS Code integrated terminal, running on Windows 11 and macOS 26.2. 

## Map of Documentation
* DS Project Repository
  * README.md
  * Data: Original Data & Final Dataset used for analysis.
    * README.md
    * ICL_NREVSS_Clinical_Labs.csv : Original data obtained from CDC FluView with filters for Virginia and Seasons 2016-17 through 2025-26. 
    * VirginiaFlu.csv : preprocessed datafile

  * Scripts:
    * 01_Preprocessing.py
    * 02_Preprocessing2.py
    * 03_Model.py
  * License
  * MODEL_OUTPUT:
  * REFERENCES

## Instruction for Reproducing results
### Software and Environment
### Reproduce Final Results: 
* Clone or download this GitHub repository....
