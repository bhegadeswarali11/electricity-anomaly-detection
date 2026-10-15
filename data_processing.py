import numpy as np
import pandas as pd

from config import OUTPUT_DIR, PROCESSED_PATH


def clean_dataset(df):
    """Clean and prepare the electricity dataset for analysis."""
    if df is None or df.empty:
        raise ValueError("Dataset is empty and cannot be processed.")

    cleaned = df.copy()
    cleaned = cleaned.drop_duplicates().reset_index(drop=True)

    for column in [
        "Consumption_kWh",
        "Occupancy",
        "Temperature_C",
        "Previous_Consumption_kWh",
    ]:
        if column in cleaned.columns:
            cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")

    if "Date" in cleaned.columns:
        cleaned["Date"] = pd.to_datetime(cleaned["Date"], errors="coerce")
    if "Time" in cleaned.columns:
        cleaned["Time"] = cleaned["Time"].astype(str).str.strip()

    for column in ["Building", "Day_Type", "Day_of_Week"]:
        if column in cleaned.columns:
            cleaned[column] = cleaned[column].fillna("Unknown").astype(str)

    if "Consumption_kWh" in cleaned.columns:
        median_consumption = cleaned["Consumption_kWh"].median()
        if pd.isna(median_consumption):
            median_consumption = 40.0
        cleaned["Consumption_kWh"] = cleaned["Consumption_kWh"].replace([np.inf, -np.inf], np.nan)
        cleaned["Consumption_kWh"] = cleaned["Consumption_kWh"].fillna(median_consumption)
        cleaned["Consumption_kWh"] = cleaned["Consumption_kWh"].clip(lower=1.0)

    for column in ["Occupancy", "Temperature_C"]:
        if column in cleaned.columns:
            median_value = cleaned[column].median()
            cleaned[column] = cleaned[column].fillna(median_value)
            cleaned[column] = cleaned[column].clip(lower=0)

    if "Previous_Consumption_kWh" in cleaned.columns:
        cleaned["Previous_Consumption_kWh"] = cleaned["Previous_Consumption_kWh"].fillna(
            cleaned["Consumption_kWh"].shift(1)
        )
        cleaned["Previous_Consumption_kWh"] = cleaned["Previous_Consumption_kWh"].replace([np.inf, -np.inf], np.nan)
        cleaned["Previous_Consumption_kWh"] = cleaned["Previous_Consumption_kWh"].fillna(
            cleaned["Consumption_kWh"]
        )
        cleaned["Previous_Consumption_kWh"] = cleaned["Previous_Consumption_kWh"].clip(lower=0.1)

    if "Building" in cleaned.columns:
        cleaned["Building"] = cleaned["Building"].replace("", "Unknown")

    cleaned = cleaned.dropna(subset=["Date", "Building", "Consumption_kWh"]).sort_values(["Date", "Building"]).reset_index(drop=True)

    if "Time" in cleaned.columns:
        cleaned["Time"] = cleaned["Time"].str.extract(r"(\d{1,2}):\d{2}").fillna("0").astype(int).astype(str)
        cleaned["Hour"] = cleaned["Time"].astype(int)

    if "Day_of_Week" not in cleaned.columns:
        cleaned["Day_of_Week"] = cleaned["Date"].dt.day_name()

    def classify_day_type(day_name):
        if day_name in ["Saturday"]:
            return "Saturday"
        if day_name in ["Sunday"]:
            return "Sunday"
        return "Weekday"

    cleaned["Day_Type"] = cleaned["Day_of_Week"].apply(classify_day_type)
    cleaned["Working_Hours"] = np.where((cleaned["Hour"] >= 8) & (cleaned["Hour"] < 18), 1, 0)

    if "Record_ID" not in cleaned.columns:
        cleaned.insert(0, "Record_ID", np.arange(1, len(cleaned) + 1))

    output_dir = OUTPUT_DIR
    output_dir.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(PROCESSED_PATH, index=False)
    return cleaned
