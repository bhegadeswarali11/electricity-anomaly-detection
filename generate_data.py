import os
from pathlib import Path

import numpy as np
import pandas as pd

from config import BUILDINGS, DATA_PATH, DATA_DIR, HOLIDAY_DATES, RANDOM_SEED


np.random.seed(RANDOM_SEED)


def get_day_type(day):
    if day.strftime("%Y-%m-%d") in HOLIDAY_DATES:
        return "Holiday"
    if day.weekday() == 5:
        return "Saturday"
    if day.weekday() == 6:
        return "Sunday"
    return "Weekday"


def building_base_consumption(building):
    base_values = {
        "Engineering Block": 50,
        "Computer Lab 1": 68,
        "Computer Lab 2": 72,
        "Library": 46,
        "Administration Block": 40,
        "Workshop": 57,
        "Canteen": 60,
        "Seminar Hall": 52,
        "Classroom Block": 38,
        "Hostel A": 32,
        "Hostel B": 34,
    }
    return base_values.get(building, 40)


def generate_dataset(force_overwrite=False, output_path=DATA_PATH):
    """Generate a realistic synthetic college electricity dataset."""
    if output_path.exists() and not force_overwrite:
        return pd.read_csv(output_path)

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    start_date = pd.Timestamp("2025-01-01")
    end_date = pd.Timestamp("2025-03-31")
    records = []
    record_id = 1

    for current_day in pd.date_range(start=start_date, end=end_date, freq="D"):
        day_type = get_day_type(current_day)
        for building in BUILDINGS:
            base_usage = building_base_consumption(building)
            for hour in range(24):
                occupancy_base = 25
                if 8 <= hour < 18:
                    occupancy_base += 55
                    if day_type == "Holiday":
                        occupancy_base -= 25
                elif 18 <= hour < 21:
                    occupancy_base += 20
                elif hour >= 22 or hour < 6:
                    occupancy_base += 5

                occupancy = np.clip(
                    np.random.normal(loc=occupancy_base, scale=18), 5, 95
                )
                temperature = np.clip(
                    np.random.normal(loc=28 + (hour / 24 * 8), scale=5), 12, 42
                )

                daytime_factor = 1.0 if 8 <= hour < 18 else 0.65 if 18 <= hour < 21 else 0.35
                day_type_factor = {
                    "Weekday": 1.10,
                    "Saturday": 0.92,
                    "Sunday": 0.78,
                    "Holiday": 0.70,
                }.get(day_type, 1.0)

                consumption = (
                    base_usage
                    * (0.55 + occupancy / 100)
                    * (0.90 + temperature / 60)
                    * daytime_factor
                    * day_type_factor
                )
                consumption += np.random.normal(0, 4.5)
                consumption = np.clip(consumption, 4, 150)

                working_hours = 1 if 8 <= hour < 18 else 0
                record = {
                    "Record_ID": record_id,
                    "Date": current_day.strftime("%Y-%m-%d"),
                    "Time": f"{hour:02d}:00",
                    "Building": building,
                    "Consumption_kWh": round(float(consumption), 2),
                    "Occupancy": round(float(occupancy), 1),
                    "Temperature_C": round(float(temperature), 1),
                    "Day_of_Week": current_day.day_name(),
                    "Day_Type": day_type,
                    "Working_Hours": working_hours,
                    "Previous_Consumption_kWh": 0.0,
                }
                records.append(record)
                record_id += 1

    df = pd.DataFrame(records)

    # The previous consumption is based on the same building's prior reading.
    df = df.sort_values(["Building", "Date", "Time"]).reset_index(drop=True)
    df["Previous_Consumption_kWh"] = (
        df.groupby("Building")["Consumption_kWh"].transform(lambda s: s.shift(1).fillna(s.iloc[0]))
    )
    df["Previous_Consumption_kWh"] = df["Previous_Consumption_kWh"].round(2)

    # Insert realistic anomalies.
    anomaly_rules = [
        ("Computer Lab 2", "02:00", 2.9),
        ("Engineering Block", "Sunday", 2.3),
        ("Library", "14:00", 2.5),
        ("Workshop", "01:00", 2.7),
        ("Computer Lab 1", "23:00", 2.4),
        ("Seminar Hall", "18:00", 2.0),
    ]

    for building, time_value, multiplier in anomaly_rules:
        mask = df["Building"].eq(building)
        if time_value == "Sunday":
            mask = mask & df["Day_of_Week"].eq("Sunday")
        else:
            mask = mask & df["Time"].eq(time_value)
        candidate_indexes = df.index[mask]
        if len(candidate_indexes) == 0:
            continue
        selected_idx = candidate_indexes[: max(1, len(candidate_indexes) // 3)]
        df.loc[selected_idx, "Consumption_kWh"] = (
            df.loc[selected_idx, "Consumption_kWh"] * multiplier
        )
        df.loc[selected_idx, "Previous_Consumption_kWh"] = df.loc[selected_idx, "Consumption_kWh"] * 0.8

    # Add repeated anomalies for some buildings to show abnormal patterns.
    repeated_buildings = ["Computer Lab 1", "Computer Lab 2", "Library"]
    for building in repeated_buildings:
        candidate_mask = df["Building"].eq(building) & df["Day_of_Week"].isin(["Sunday", "Saturday"])
        candidate_index = df.index[candidate_mask]
        if len(candidate_index) > 0:
            sample_idx = candidate_index[: min(8, len(candidate_index))]
            df.loc[sample_idx, "Consumption_kWh"] = df.loc[sample_idx, "Consumption_kWh"] * 1.7
            df.loc[sample_idx, "Previous_Consumption_kWh"] = df.loc[sample_idx, "Consumption_kWh"] * 0.9

    # Ensure values remain in a realistic positive range.
    df["Consumption_kWh"] = np.clip(df["Consumption_kWh"], 4.0, 200.0)
    df["Occupancy"] = np.clip(df["Occupancy"], 5.0, 100.0)
    df["Temperature_C"] = np.clip(df["Temperature_C"], 10.0, 45.0)

    df.to_csv(output_path, index=False)
    return df


if __name__ == "__main__":
    generate_dataset(force_overwrite=True)
    print(f"Dataset generated at: {DATA_PATH}")
