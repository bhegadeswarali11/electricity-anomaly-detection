import pandas as pd


def generate_alerts(df):
    """Create user-friendly alerts from anomaly results."""
    alerts = []

    if df.empty:
        return alerts

    for _, row in df[df["AI_Status"] == "Anomaly"].iterrows():
        building = row["Building"]
        date = row["Date"]
        time_val = row["Time"]
        consumption = row["Consumption_kWh"]
        hour = row.get("Hour", 0)

        severity = "Warning"
        if row.get("AI_Score", 0) < -0.2:
            severity = "Critical"

        if (hour < 8) or (hour >= 18):
            reason = "AI detected unusually high electricity consumption outside normal working hours."
            recommendation = "Inspect whether equipment, lights, or air conditioning were left running after hours."
        elif row["Day_Type"] in ["Saturday", "Sunday"]:
            reason = "AI detected unusual electricity usage during a weekend or holiday period."
            recommendation = "Check whether building systems were left active beyond normal campus usage."
        elif consumption > df["Consumption_kWh"].quantile(0.95):
            reason = "AI detected a sudden spike compared with the usual consumption pattern."
            recommendation = "Review equipment loads and look for unusual operational activity in the building."
        else:
            reason = "AI detected an abnormal consumption pattern compared with the building’s normal trend."
            recommendation = "Inspect operations in the building and verify whether equipment usage is expected."

        alerts.append({
            "Severity": severity,
            "Building": building,
            "Date": date,
            "Time": time_val,
            "Consumption": round(float(consumption), 2),
            "Reason": reason,
            "Recommendation": recommendation,
        })

    # Deduplicate repeated anomalies by building and hour for readability.
    deduped = []
    seen = set()
    for alert in alerts:
        key = (alert["Building"], alert["Date"], alert["Time"])
        if key not in seen:
            deduped.append(alert)
            seen.add(key)

    return deduped


def summarize_alerts(alerts):
    """Summarize alert counts by severity."""
    summary = {"Normal": 0, "Info": 0, "Warning": 0, "Critical": 0}
    for alert in alerts:
        summary[alert["Severity"]] = summary.get(alert["Severity"], 0) + 1
    return summary
