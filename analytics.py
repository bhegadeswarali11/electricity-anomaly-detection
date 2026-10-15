import numpy as np
import pandas as pd


def calculate_statistics(df):
    """Compute useful electricity consumption statistics."""
    stats = {
        "total_consumption": df["Consumption_kWh"].sum(),
        "average_consumption": df["Consumption_kWh"].mean(),
        "median_consumption": df["Consumption_kWh"].median(),
        "std_deviation": df["Consumption_kWh"].std(),
        "min_consumption": df["Consumption_kWh"].min(),
        "max_consumption": df["Consumption_kWh"].max(),
        "variance": df["Consumption_kWh"].var(),
        "building_average": df.groupby("Building")["Consumption_kWh"].mean().sort_values(ascending=False),
        "hourly_average": df.groupby("Hour")["Consumption_kWh"].mean().sort_index(),
        "daily_average": df.groupby("Date")["Consumption_kWh"].mean(),
        "weekend_average": df[df["Day_Type"].isin(["Saturday", "Sunday"])]["Consumption_kWh"].mean(),
        "weekday_average": df[df["Day_Type"] == "Weekday"]["Consumption_kWh"].mean(),
    }
    return stats


def filter_dataframe(df, building=None, start_date=None, end_date=None, day_type="All", ai_status="All"):
    """Filter the dataset according to user selections."""
    filtered = df.copy()

    if building and building != "All":
        filtered = filtered[filtered["Building"] == building]
    if start_date is not None:
        filtered = filtered[filtered["Date"] >= pd.to_datetime(start_date)]
    if end_date is not None:
        filtered = filtered[filtered["Date"] <= pd.to_datetime(end_date)]
    if day_type != "All":
        filtered = filtered[filtered["Day_Type"] == day_type]
    if ai_status != "All":
        filtered = filtered[filtered["AI_Status"] == ai_status]

    return filtered


def get_building_summary(df, building):
    """Return a summary of a selected building."""
    building_data = df[df["Building"] == building]
    return {
        "total_consumption": building_data["Consumption_kWh"].sum(),
        "average_consumption": building_data["Consumption_kWh"].mean(),
        "peak_usage": building_data["Consumption_kWh"].max(),
        "num_anomalies": int((building_data["AI_Status"] == "Anomaly").sum()),
        "daily_trend": building_data.groupby("Date")["Consumption_kWh"].sum().sort_index(),
        "hourly_pattern": building_data.groupby("Hour")["Consumption_kWh"].mean().sort_index(),
        "after_hours": building_data[(building_data["Hour"] < 8) | (building_data["Hour"] >= 18)],
    }


def get_peak_usage_hour(df):
    """Return the hour with the highest average consumption."""
    if df.empty:
        return "N/A"
    peak = df.groupby("Hour")["Consumption_kWh"].mean().idxmax()
    return f"{int(peak):02d}:00"
