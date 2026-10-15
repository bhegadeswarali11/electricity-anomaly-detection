import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

from config import CONTAMINATION


def prepare_feature_matrix(df):
    """Prepare numeric features for the Isolation Forest model."""
    features = [
        "Consumption_kWh",
        "Occupancy",
        "Temperature_C",
        "Hour",
        "Working_Hours",
        "Previous_Consumption_kWh",
    ]
    required = [col for col in features if col in df.columns]
    return df[required].copy()


def run_isolation_forest(df, contamination=CONTAMINATION):
    """Run Isolation Forest to detect unusual consumption patterns."""
    if df is None or df.empty:
        raise ValueError("Dataset is empty. Unable to run the AI model.")

    features_df = prepare_feature_matrix(df)
    if features_df.empty:
        raise ValueError("No valid feature data available for anomaly detection.")

    model = IsolationForest(
        n_estimators=200,
        contamination=contamination,
        random_state=42,
        n_jobs=-1,
    )
    labels = model.fit_predict(features_df)

    result = df.copy()
    result["AI_Score"] = model.score_samples(features_df)
    result["AI_Label"] = labels
    result["AI_Status"] = np.where(result["AI_Label"] == -1, "Anomaly", "Normal")
    result["Anomaly_Score"] = np.abs(result["AI_Score"])
    return result, model


def get_anomaly_summary(df):
    """Return anomaly counts and percentages."""
    total = len(df)
    anomalies = int((df["AI_Status"] == "Anomaly").sum())
    normal = total - anomalies
    pct = (anomalies / total) * 100 if total else 0
    return {
        "total": total,
        "anomalies": anomalies,
        "normal": normal,
        "percentage": pct,
    }
