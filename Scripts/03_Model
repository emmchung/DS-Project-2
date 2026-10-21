# Virginia Influenza Forecasting - SARIMA Model
#
# This script develops and evaluates a Seasonal Autoregressive
# Integrated Moving Average (SARIMA) model to forecast weekly
# influenza positivity and predict seasonal peak timing in Virginia.
#
# Using preprocessed CDC FluView data from the 2016-17 through
# 2025-26 influenza seasons, the script performs a chronological
# 80/20 train-test split, selects SARIMA parameters using AIC,
# and generates forecasts for the two held-out influenza seasons.
# Model performance is evaluated using MAE, RMSE, and seasonal
# peak timing and magnitude errors, with comparisons to a
# seasonal-naive baseline.
#
# Input: Data/VirginiaFlu.csv
# Output: Output/ (model comparisons, forecast predictions,
#         evaluation summaries, and diagnostic figures)
#
# Required libraries: pandas, numpy, matplotlib, statsmodels
# Run from the repository root: python train_model.py

import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.stats.diagnostic import acorr_ljungbox


# Define input and output file locations
INPUT_FILE = "Data/VirginiaFlu.csv"
OUTPUT_DIR = Path("Output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# LOAD AND VALIDATE DATA

# Load the preprocessed dataset and convert week_start to dates
df = pd.read_csv(INPUT_FILE, parse_dates=["week_start"])

# Verify that the variables required for modeling are present
required_columns = [
    "week_start", "season", "season_week",
    "percent_positive"
]

if not set(required_columns).issubset(df.columns):
    raise ValueError("Required columns are missing.")

# Check for missing values in the required columns
if df[required_columns].isna().any().any():
    raise ValueError("Missing values detected.")

# Sort observations chronologically and check for duplicate dates
df = df.sort_values("week_start").reset_index(drop=True)

if df["week_start"].duplicated().any():
    raise ValueError("Duplicate weekly dates detected.")

# Verify that observations occur at regular seven-day intervals
if not df["week_start"].diff().dropna().eq(
    pd.Timedelta(days=7)
).all():
    raise ValueError("Missing or irregular weekly dates.")

# Verify that influenza positivity percentages are between 0 and 100
if not df["percent_positive"].between(0, 100).all():
    raise ValueError("Invalid positivity percentages.")

# Confirm that all ten influenza seasons are included
expected_seasons = [
    f"{year}-{year + 1}"
    for year in range(2016, 2026)
]

actual_seasons = sorted(df["season"].unique())

if actual_seasons != expected_seasons:
    raise ValueError(
        f"Expected 10 seasons, found: {actual_seasons}"
    )

# Set the weekly date as the time-series index
df = df.set_index("week_start").asfreq("W-SUN")

print("\nDATASET SUMMARY")
print("Total observations:", len(df))
print(df.groupby("season").size())


# CHRONOLOGICAL TRAIN-TEST SPLIT

# Use the first eight seasons for training and the final two for testing
# This preserves chronological order and prevents using future data for training
train = df[
    df["season"] <= "2023-2024"
].copy()

test = df[
    df["season"].isin(["2024-2025", "2025-2026"])
].copy()

# Verify that the testing period begins immediately after training
if train.index.max() + pd.Timedelta(days=7) != test.index.min():
    raise ValueError("Gap between training and testing periods.")

# Define weekly influenza positivity as the forecasting variable
y_train = train["percent_positive"].astype(float)
y_test = test["percent_positive"].astype(float)

print("\nTRAIN-TEST SPLIT")
print("Training observations:", len(y_train))
print("Testing observations:", len(y_test))
print("Training seasons:", train["season"].nunique())
print("Testing seasons:", test["season"].nunique())


# SARIMA MODEL SELECTION

# Test combinations of nonseasonal and seasonal SARIMA parameters
# The seasonal period of 52 represents approximately one influenza year
# Models are compared using AIC, with selection based on training data only
candidate_orders = [
    (0, 0, 1),
    (1, 0, 0),
    (1, 0, 1),
    (0, 1, 1),
    (1, 1, 0),
    (1, 1, 1)
]

candidate_seasonal_orders = [
    (0, 1, 1, 52),
    (1, 1, 0, 52)
]

# Store the results of successfully fitted candidate models
model_results = []

print("\nSTARTING SARIMA MODEL SELECTION")

total_models = (
    len(candidate_orders) *
    len(candidate_seasonal_orders)
)

model_number = 0

# Fit each candidate model and record its AIC and BIC
for order in candidate_orders:
    for seasonal_order in candidate_seasonal_orders:

        model_number += 1

        print(
            f"Testing model {model_number}/{total_models}: "
            f"{order} {seasonal_order}",
            flush=True
        )

        try:
            # Suppress fitting warnings while testing model combinations
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")

                model = SARIMAX(
                    y_train,
                    order=order,
                    seasonal_order=seasonal_order,
                    trend="n",
                    enforce_stationarity=False,
                    enforce_invertibility=False
                )

                result = model.fit(
                    disp=False,
                    maxiter=100
                )

            # Retain models that converged and produced a valid AIC
            if (
                result.mle_retvals.get("converged", False)
                and np.isfinite(result.aic)
            ):
                model_results.append({
                    "order": str(order),
                    "seasonal_order": str(seasonal_order),
                    "AIC": result.aic,
                    "BIC": result.bic,
                    "order_values": order,
                    "seasonal_values": seasonal_order
                })

        except Exception as error:
            print("Model failed:", error)

# Stop if none of the candidate models converged
if not model_results:
    raise RuntimeError("No candidate SARIMA models converged.")

# Rank successful models by AIC and select the lowest value
comparison = pd.DataFrame(model_results)
comparison = comparison.sort_values(
    "AIC"
).reset_index(drop=True)

best = comparison.iloc[0]

best_order = best["order_values"]
best_seasonal_order = best["seasonal_values"]

# Save the model comparison results for reproducibility
comparison.drop(
    columns=["order_values", "seasonal_values"]
).to_csv(
    OUTPUT_DIR / "sarima_model_comparison.csv",
    index=False
)

print("\nSELECTED SARIMA MODEL")
print("Order:", best_order)
print("Seasonal order:", best_seasonal_order)
print("AIC:", best["AIC"])


# FIT FINAL SARIMA MODEL

# Refit the selected SARIMA configuration using all training observations
with warnings.catch_warnings():
    warnings.simplefilter("ignore")

    model = SARIMAX(
        y_train,
        order=best_order,
        seasonal_order=best_seasonal_order,
        trend="n",
        enforce_stationarity=False,
        enforce_invertibility=False
    )

    fitted_model = model.fit(
        disp=False,
        maxiter=200
    )

# Confirm that the final model converged
if not fitted_model.mle_retvals.get("converged", False):
    raise RuntimeError("Final model did not converge.")


# FORECAST TESTING PERIOD

# Generate one forecast covering both testing seasons without
# updating the model using actual testing observations
forecast_result = fitted_model.get_forecast(
    steps=len(y_test)
)

# Restrict predicted positivity percentages to the valid 0-100 range
sarima_pred = pd.Series(
    forecast_result.predicted_mean.to_numpy(),
    index=y_test.index
).clip(lower=0, upper=100)


# SEASONAL-NAIVE BASELINE

# Create a baseline by repeating the last 52 observed training weeks
# This approximates annual seasonality, including years with 53 CDC weeks
last_52_weeks = y_train.iloc[-52:].to_numpy()

naive_values = np.resize(
    last_52_weeks,
    len(y_test)
)

naive_pred = pd.Series(
    naive_values,
    index=y_test.index
)


# SAVE WEEKLY FORECAST PREDICTIONS

# Combine actual positivity and both model predictions for each testing week
forecast_df = pd.DataFrame({
    "season": test["season"],
    "season_week": test["season_week"],
    "actual_positivity": y_test,
    "sarima_prediction": sarima_pred,
    "naive_prediction": naive_pred
})

# Save weekly predictions for evaluation and visualization
forecast_df.to_csv(
    OUTPUT_DIR / "weekly_forecast_predictions.csv",
    index_label="week_start"
)


# EVALUATE WEEKLY FORECAST ACCURACY

# Calculate mean absolute error (MAE) and root mean squared error (RMSE)
# Lower values indicate predictions closer to observed positivity
def calculate_metrics(actual, predicted):

    actual = np.asarray(actual)
    predicted = np.asarray(predicted)

    errors = actual - predicted

    mae = np.mean(np.abs(errors))
    rmse = np.sqrt(np.mean(errors ** 2))

    return mae, rmse


accuracy_results = []

# Evaluate SARIMA and the baseline separately for each testing season
for model_name, predictions in [
    ("SARIMA", sarima_pred),
    ("Seasonal Naive", naive_pred)
]:

    for season in ["2024-2025", "2025-2026"]:

        mask = test["season"] == season

        mae, rmse = calculate_metrics(
            y_test.loc[mask],
            predictions.loc[mask]
        )

        accuracy_results.append({
            "model": model_name,
            "season": season,
            "MAE": mae,
            "RMSE": rmse
        })

    # Also calculate accuracy across the full testing period
    overall_mae, overall_rmse = calculate_metrics(
        y_test, predictions
    )

    accuracy_results.append({
        "model": model_name,
        "season": "Overall",
        "MAE": overall_mae,
        "RMSE": overall_rmse
    })

# Save accuracy results for both models
accuracy_df = pd.DataFrame(accuracy_results)

accuracy_df.to_csv(
    OUTPUT_DIR / "forecast_accuracy_summary.csv",
    index=False
)

print("\nFORECAST ACCURACY")
print(accuracy_df.to_string(index=False))


# EVALUATE SEASONAL PEAK PREDICTIONS

# Compare the predicted and actual peak week and peak positivity
# for each testing season
peak_results = []

for season in ["2024-2025", "2025-2026"]:

    season_data = forecast_df[
        forecast_df["season"] == season
    ]

    # Identify the actual peak date and positivity percentage
    actual_peak_date = season_data[
        "actual_positivity"
    ].idxmax()

    actual_peak_value = season_data.loc[
        actual_peak_date, "actual_positivity"
    ]

    for model_name, column in [
        ("SARIMA", "sarima_prediction"),
        ("Seasonal Naive", "naive_prediction")
    ]:

        # Identify the predicted peak date and positivity percentage
        predicted_peak_date = season_data[
            column
        ].idxmax()

        predicted_peak_value = season_data.loc[
            predicted_peak_date, column
        ]

        # Calculate timing error in weeks (positive means a later peak)
        timing_error = (
            predicted_peak_date - actual_peak_date
        ).days / 7

        # Record signed and absolute peak timing and magnitude errors
        peak_results.append({
            "model": model_name,
            "season": season,
            "actual_peak_date": actual_peak_date,
            "predicted_peak_date": predicted_peak_date,
            "actual_peak_positivity": actual_peak_value,
            "predicted_peak_positivity": predicted_peak_value,
            "timing_error_weeks": timing_error,
            "absolute_timing_error_weeks": abs(timing_error),
            "peak_magnitude_error": (
                predicted_peak_value - actual_peak_value
            ),
            "absolute_peak_magnitude_error": abs(
                predicted_peak_value - actual_peak_value
            )
        })

# Save seasonal peak prediction results
peak_df = pd.DataFrame(peak_results)

peak_df.to_csv(
    OUTPUT_DIR / "seasonal_peak_results.csv",
    index=False
)

print("\nSEASONAL PEAK RESULTS")
print(peak_df.to_string(index=False))


# FIGURE: ACTUAL VS PREDICTED POSITIVITY

# Plot training data, observed testing values, and both forecasts
# to visualize overall forecasting performance
plt.figure(figsize=(12, 6))

plt.plot(
    y_train.index,
    y_train,
    label="Training data",
    alpha=0.5
)

plt.plot(
    y_test.index,
    y_test,
    label="Actual test positivity",
    linewidth=2
)

plt.plot(
    sarima_pred.index,
    sarima_pred,
    label="SARIMA forecast",
    linewidth=2
)

plt.plot(
    naive_pred.index,
    naive_pred,
    label="Seasonal-naive forecast",
    linestyle="--"
)

# Mark the boundary between training and testing periods
plt.axvline(
    y_test.index.min(),
    color="gray",
    linestyle=":",
    label="Train-test split"
)

plt.title("Virginia Influenza Positivity: SARIMA Forecast")
plt.xlabel("Date")
plt.ylabel("Influenza Positivity (%)")
plt.legend()
plt.tight_layout()

# Save the overall forecast comparison figure
plt.savefig(
    OUTPUT_DIR / "influenza_forecast_comparison.png",
    dpi=300
)

plt.close()


# FIGURE: SEASONAL PEAK COMPARISON

# Create separate plots for the two testing seasons to compare
# actual and predicted influenza peaks
fig, axes = plt.subplots(
    1, 2, figsize=(13, 5),
    sharey=True
)

for ax, season in zip(
    axes, ["2024-2025", "2025-2026"]
):

    subset = forecast_df[
        forecast_df["season"] == season
    ]

    ax.plot(
        subset["season_week"],
        subset["actual_positivity"],
        label="Actual",
        linewidth=2
    )

    ax.plot(
        subset["season_week"],
        subset["sarima_prediction"],
        label="SARIMA",
        linewidth=2
    )

    ax.plot(
        subset["season_week"],
        subset["naive_prediction"],
        label="Seasonal naive",
        linestyle="--"
    )

    # Identify the actual and SARIMA-predicted peak weeks
    actual_peak = subset["actual_positivity"].idxmax()
    sarima_peak = subset["sarima_prediction"].idxmax()

    # Mark the peak locations on each graph
    ax.scatter(
        subset.loc[actual_peak, "season_week"],
        subset.loc[actual_peak, "actual_positivity"],
        marker="o",
        s=70,
        label="Actual peak"
    )

    ax.scatter(
        subset.loc[sarima_peak, "season_week"],
        subset.loc[sarima_peak, "sarima_prediction"],
        marker="x",
        s=90,
        label="SARIMA peak"
    )

    ax.set_title(season)
    ax.set_xlabel("Week within influenza season")
    ax.grid(alpha=0.2)

axes[0].set_ylabel("Influenza Positivity (%)")

handles, labels = axes[0].get_legend_handles_labels()

fig.legend(
    handles, labels,
    loc="lower center",
    ncol=5
)

fig.suptitle("Seasonal Influenza Peak Prediction")
fig.tight_layout(rect=[0, 0.12, 1, 0.94])

# Save the seasonal peak comparison figure
plt.savefig(
    OUTPUT_DIR / "seasonal_peak_comparison.png",
    dpi=300
)

plt.close()


# MODEL RESIDUAL DIAGNOSTICS

# Examine model residuals to identify remaining patterns or autocorrelation
# Exclude the first 52 observations to reduce initialization effects
residuals = fitted_model.resid.iloc[52:].dropna()

# Run Ljung-Box tests at lags 10 and 20 to assess residual autocorrelation
ljung_box = acorr_ljungbox(
    residuals,
    lags=[10, 20],
    return_df=True
)

# Generate diagnostic plots of residual behavior and distribution
diagnostic_figure = fitted_model.plot_diagnostics(
    figsize=(12, 8)
)

diagnostic_figure.tight_layout()

# Save residual diagnostic plots
diagnostic_figure.savefig(
    OUTPUT_DIR / "sarima_residual_diagnostics.png",
    dpi=300
)

plt.close(diagnostic_figure)


# SAVE TEXT SUMMARY

# Extract overall accuracy and seasonal peak results for both models
sarima_accuracy = accuracy_df[
    (accuracy_df["model"] == "SARIMA") &
    (accuracy_df["season"] == "Overall")
].iloc[0]

naive_accuracy = accuracy_df[
    (accuracy_df["model"] == "Seasonal Naive") &
    (accuracy_df["season"] == "Overall")
].iloc[0]

sarima_peaks = peak_df[
    peak_df["model"] == "SARIMA"
]

naive_peaks = peak_df[
    peak_df["model"] == "Seasonal Naive"
]

# Write a summary of the dataset, selected model, forecast accuracy,
# seasonal peak errors, and residual diagnostics to a text file
with open(
    OUTPUT_DIR / "model_results_summary.txt",
    "w",
    encoding="utf-8"
) as file:

    file.write("VIRGINIA INFLUENZA SARIMA MODEL\n")
    file.write("=" * 45 + "\n\n")

    file.write("DATASET\n")
    file.write(f"Total observations: {len(df)}\n")
    file.write(f"Training observations: {len(train)}\n")
    file.write(f"Testing observations: {len(test)}\n")
    file.write("Training: 2016-17 through 2023-24\n")
    file.write("Testing: 2024-25 through 2025-26\n\n")

    file.write("SELECTED MODEL\n")
    file.write(f"SARIMA order: {best_order}\n")
    file.write(
        f"Seasonal order: {best_seasonal_order}\n"
    )
    file.write(f"AIC: {best['AIC']:.3f}\n\n")

    file.write("OVERALL FORECAST ACCURACY\n")
    file.write(
        f"SARIMA MAE: {sarima_accuracy['MAE']:.3f}\n"
    )
    file.write(
        f"SARIMA RMSE: {sarima_accuracy['RMSE']:.3f}\n"
    )
    file.write(
        f"Baseline MAE: {naive_accuracy['MAE']:.3f}\n"
    )
    file.write(
        f"Baseline RMSE: {naive_accuracy['RMSE']:.3f}\n\n"
    )

    file.write("SEASONAL PEAK ACCURACY\n")
    file.write(
        "SARIMA mean absolute peak timing error: "
        f"{sarima_peaks['absolute_timing_error_weeks'].mean():.2f} weeks\n"
    )
    file.write(
        "Baseline mean absolute peak timing error: "
        f"{naive_peaks['absolute_timing_error_weeks'].mean():.2f} weeks\n"
    )
    file.write(
        "SARIMA mean absolute peak magnitude error: "
        f"{sarima_peaks['absolute_peak_magnitude_error'].mean():.3f} "
        "percentage points\n"
    )
    file.write(
        "Baseline mean absolute peak magnitude error: "
        f"{naive_peaks['absolute_peak_magnitude_error'].mean():.3f} "
        "percentage points\n\n"
    )

    file.write("LJUNG-BOX RESIDUAL TEST\n")
    file.write(ljung_box.to_string())
    file.write("\n\n")

    file.write("MODEL SUMMARY\n")
    file.write(str(fitted_model.summary()))

print("\nMODELING COMPLETED SUCCESSFULLY")
print("All results saved to:", OUTPUT_DIR)
