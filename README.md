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
     * forecast_accuracy_summary.csv: Accuracy of **positivity** prediction (MAE, RMSE)
     * influenza_forecast_comparison.png
     * model_results_summary.txt: Summarizes model results.
     * sarima_model_comparison.csv: Model selection
     * sarima_residual_diagnostics.png
     * seasonal_peak_comparison.png
     * seasonal_peak_results.csv: Accuracy of **peak** prediction (# of weeks)
     * weekly_forecast_predictions.csv: actual model prediction
  * REFERENCES

## Instruction for Reproducing results
### Software and Environment
### Software and Environment
- Python 3.13
- Visual Studio Code (VS Code)
- Required Python packages:
  - pandas 3.0.3
  - numpy 2.4.6
  - matplotlib 3.11.2
  - statsmodels 0.15.0
 
Install the required packages by running:
 ```bash
pip install pandas numpy matplotlib statsmodels
```
### Reproduce Final Results

The preprocessed Virginia influenza dataset required for modeling is provided in the `Data` folder. **Users do not need to download or preprocess the original CDC FluView dataset** to reproduce the final modeling results.

1. **Clone or download** this GitHub repository and open the project folder in Visual Studio Code.

2. **Confirm that the required dataset is available:**
   - `Data/VirginiaFlu.csv`

3. **Install the required Python packages** using the command provided in the Software and Environment section above.

4. **Run the modeling script** from the repository's root directory:

   ```bash
   python train_model.py
   ```

5. **The modeling script will:**
   - Load and validate the preprocessed Virginia influenza dataset.
   - Split the data chronologically into **training (2016-17 through 2023-24)** and **testing (2024-25 through 2025-26)** seasons.
   - Develop and select a **SARIMA model** based on Akaike Information Criterion (AIC).
   - Generate weekly influenza positivity forecasts and compare them against a **seasonal-naive baseline**.
   - Evaluate forecast accuracy using **MAE, RMSE, and seasonal peak timing and magnitude errors**.
   - Generate forecast comparison figures, residual diagnostics, and summary results.

6. **View the generated results** in the `Output` folder, including forecast predictions, performance metrics, figures, and summary files.
