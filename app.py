from __future__ import annotations

import os
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd
import streamlit as st

from alerts import generate_alerts
from analytics import calculate_statistics, filter_dataframe, get_building_summary, get_peak_usage_hour
from anomaly_detection import get_anomaly_summary, run_isolation_forest
from config import BUILDINGS, DATA_PATH, OUTPUT_DIR, PROCESSED_PATH
from data_loader import load_dataset
from data_processing import clean_dataset
from generate_data import generate_dataset
from visualization import (
    plot_anomaly_distribution,
    plot_anomaly_timeline,
    plot_building_consumption,
    plot_consumption_distribution,
    plot_consumption_trend,
    plot_hourly_consumption,
    plot_occupancy_vs_consumption,
)

matplotlib.use("Agg")

st.set_page_config(
    page_title="AI College Electricity Monitor",
    page_icon="⚡",
    layout="wide",
)


def ensure_project_files():
    """Create required project folders and dataset if missing."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    if not DATA_PATH.exists():
        generate_dataset(force_overwrite=False, output_path=DATA_PATH)


def load_processed_data():
    """Load, clean, and process the dataset automatically."""
    ensure_project_files()
    raw_df = load_dataset(DATA_PATH)
    cleaned = clean_dataset(raw_df)
    processed, _ = run_isolation_forest(cleaned)
    processed["AI_Status"] = processed["AI_Status"].replace({"Anomaly": "Anomaly", "Normal": "Normal"})
    processed["Date"] = pd.to_datetime(processed["Date"])
    processed.to_csv(PROCESSED_PATH, index=False)
    return processed


def show_dashboard(df):
    """Render the main dashboard page."""
    stats = calculate_statistics(df)
    anomaly_summary = get_anomaly_summary(df)
    alerts = generate_alerts(df)
    peak_hour = get_peak_usage_hour(df)

    st.title("⚡ AI-Based College Electricity Consumption & Anomaly Detection System")
    st.caption("Intelligent electricity monitoring, consumption analytics and anomaly detection")

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.metric("Total Consumption", f"{stats['total_consumption']:,.0f} kWh")
    with col2:
        st.metric("Average Consumption", f"{stats['average_consumption']:.1f} kWh")
    with col3:
        st.metric("AI Anomalies", f"{anomaly_summary['anomalies']}")
    with col4:
        highest_building = stats["building_average"].idxmax() if not stats["building_average"].empty else "N/A"
        st.metric("Highest Consumption Building", highest_building)
    with col5:
        st.metric("Peak Usage Hour", peak_hour)
    with col6:
        after_hours = df[(df["Hour"] < 8) | (df["Hour"] >= 18)]
        st.metric("After-Hours Anomalies", int((after_hours["AI_Status"] == "Anomaly").sum()))

    st.subheader("Overall Consumption Trend")
    st.pyplot(plot_consumption_trend(df))

    recent = df.sort_values("Date", ascending=False).head(10)
    st.subheader("Recent Alerts")
    if alerts:
        for alert in alerts[:5]:
            with st.container():
                severity = alert["Severity"]
                if severity == "Critical":
                    st.error(f"{severity} | {alert['Building']} | {alert['Date']} | {alert['Time']} | {alert['Consumption']} kWh")
                elif severity == "Warning":
                    st.warning(f"{severity} | {alert['Building']} | {alert['Date']} | {alert['Time']} | {alert['Consumption']} kWh")
                else:
                    st.info(f"{severity} | {alert['Building']} | {alert['Date']} | {alert['Time']} | {alert['Consumption']} kWh")
    else:
        st.success("No abnormal electricity patterns detected in the current dataset.")

    st.subheader("Normal vs Anomaly Summary")
    normal_count = int((df["AI_Status"] == "Normal").sum())
    anomaly_count = int((df["AI_Status"] == "Anomaly").sum())
    st.bar_chart(pd.DataFrame({"Status": ["Normal", "Anomaly"], "Count": [normal_count, anomaly_count]}).set_index("Status"))

    st.subheader("How does the AI detect anomalies?")
    st.info(
        "The system uses Isolation Forest, an unsupervised machine learning algorithm. It learns the general pattern of electricity consumption from the available data and identifies records that are significantly different from the usual pattern. These records are marked as anomalies and displayed as alerts for further inspection."
    )


def show_consumption_analysis(df):
    """Render the consumption analysis page."""
    st.title("📊 Consumption Analysis")
    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(plot_consumption_trend(df))
    with col2:
        st.pyplot(plot_building_consumption(df))

    col1, col2 = st.columns(2)
    with col1:
        st.pyplot(plot_hourly_consumption(df))
    with col2:
        st.pyplot(plot_consumption_distribution(df))

    st.subheader("Weekday vs Weekend Comparison")
    daily_summary = df.groupby("Day_Type")["Consumption_kWh"].mean().sort_values(ascending=False)
    st.bar_chart(daily_summary)

    st.subheader("Occupancy vs Consumption")
    st.pyplot(plot_occupancy_vs_consumption(df))


def show_anomaly_detection(df):
    """Render the anomaly detection page."""
    st.title("🤖 AI Anomaly Detection")
    summary = get_anomaly_summary(df)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Records", summary["total"])
    with col2:
        st.metric("Normal Records", summary["normal"])
    with col3:
        st.metric("Anomaly Records", summary["anomalies"])

    st.metric("Anomaly Percentage", f"{summary['percentage']:.2f}%")
    st.pyplot(plot_anomaly_distribution(df))
    st.pyplot(plot_anomaly_timeline(df))

    st.subheader("Anomaly Table")
    anomaly_table = df[df["AI_Status"] == "Anomaly"][[
        "Date",
        "Time",
        "Building",
        "Consumption_kWh",
        "Occupancy",
        "Temperature_C",
        "AI_Score",
        "AI_Status",
    ]].copy()
    anomaly_table = anomaly_table.sort_values("Consumption_kWh", ascending=False)
    anomaly_table["Date"] = anomaly_table["Date"].dt.strftime("%Y-%m-%d")
    st.dataframe(anomaly_table, use_container_width=True)

    st.subheader("Building-wise Anomaly Count")
    anomaly_by_building = (
        df.assign(Is_Anomaly=df["AI_Status"].eq("Anomaly"))
        .groupby("Building")["Is_Anomaly"]
        .sum()
        .sort_values(ascending=False)
    )
    st.bar_chart(anomaly_by_building)

    st.subheader("Anomaly Score")
    anomaly_score_by_day = df.groupby(pd.to_datetime(df["Date"]))["AI_Score"].mean().sort_index()
    st.line_chart(anomaly_score_by_day)


def show_building_analysis(df):
    """Render the building analysis page."""
    st.title("🏢 Building Analysis")
    building = st.selectbox("Select a building", ["All"] + sorted(df["Building"].unique().tolist()))
    if building == "All":
        building_df = df
    else:
        building_df = df[df["Building"] == building]

    if building_df.empty:
        st.warning("No data available for the selected building.")
        return

    summary = get_building_summary(building_df, building) if building != "All" else {
        "total_consumption": building_df["Consumption_kWh"].sum(),
        "average_consumption": building_df["Consumption_kWh"].mean(),
        "peak_usage": building_df["Consumption_kWh"].max(),
        "num_anomalies": int((building_df["AI_Status"] == "Anomaly").sum()),
        "daily_trend": building_df.groupby("Date")["Consumption_kWh"].sum().sort_index(),
        "hourly_pattern": building_df.groupby("Hour")["Consumption_kWh"].mean().sort_index(),
        "after_hours": building_df[(building_df["Hour"] < 8) | (building_df["Hour"] >= 18)],
    }

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Consumption", f"{summary['total_consumption']:.1f} kWh")
    with col2:
        st.metric("Average Consumption", f"{summary['average_consumption']:.1f} kWh")
    with col3:
        st.metric("Peak Usage", f"{summary['peak_usage']:.1f} kWh")
    with col4:
        st.metric("Number of Anomalies", summary["num_anomalies"])

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Daily Trend")
        st.line_chart(summary["daily_trend"])
    with col2:
        st.subheader("Hourly Pattern")
        st.line_chart(summary["hourly_pattern"])

    st.subheader("After-Hours Usage")
    st.dataframe(summary["after_hours"].head(20), use_container_width=True)


def show_alerts_page(df):
    """Render the alerts and recommendations page."""
    st.title("🚨 Alerts & Recommendations")
    alerts = generate_alerts(df)
    if not alerts:
        st.success("No alerts generated. The current dataset appears normal.")
        return

    for alert in alerts:
        severity = alert["Severity"]
        color = "normal"
        if severity == "Critical":
            color = "red"
        elif severity == "Warning":
            color = "orange"
        elif severity == "Info":
            color = "blue"

        st.markdown(f"### {severity} - {alert['Building']}")
        st.write(f"Date: {alert['Date']}")
        st.write(f"Time: {alert['Time']}")
        st.write(f"Consumption: {alert['Consumption']} kWh")
        st.write(f"Reason: {alert['Reason']}")
        st.write(f"Recommendation: {alert['Recommendation']}")
        st.markdown("---")


def show_data_explorer(df):
    """Render the data explorer page."""
    st.title("🔎 Data Explorer")
    building_filter = st.selectbox("Building", ["All"] + sorted(df["Building"].unique()))
    date_min = pd.to_datetime(df["Date"]).min()
    date_max = pd.to_datetime(df["Date"]).max()
    start_date = st.date_input("Start date", value=date_min.date())
    end_date = st.date_input("End date", value=date_max.date())
    ai_status = st.selectbox("AI Status", ["All", "Normal", "Anomaly"])
    search = st.text_input("Search keyword")

    filtered = df.copy()
    if building_filter != "All":
        filtered = filtered[filtered["Building"] == building_filter]
    filtered["Date"] = pd.to_datetime(filtered["Date"])
    filtered = filtered[filtered["Date"] >= pd.to_datetime(start_date)]
    filtered = filtered[filtered["Date"] <= pd.to_datetime(end_date)]
    if ai_status != "All":
        filtered = filtered[filtered["AI_Status"] == ai_status]
    if search:
        row_text = filtered.astype(str).agg(" ".join, axis=1)
        filtered = filtered[row_text.str.contains(search, case=False, regex=False)]

    filtered["Date"] = filtered["Date"].dt.strftime("%Y-%m-%d")
    st.dataframe(filtered, use_container_width=True)
    csv_data = filtered.to_csv(index=False).encode("utf-8")
    st.download_button("Download Processed CSV", data=csv_data, file_name="processed_electricity_data.csv", mime="text/csv")


def show_about_page():
    """Render the project description page."""
    st.title("📘 About Project")
    st.write("This project analyzes college electricity consumption data and uses an unsupervised AI model to find unusual patterns.")
    st.write("The system does not physically inspect electrical equipment; it only studies consumption patterns from historical data.")
    st.subheader("Problem Statement")
    st.write("Colleges often face high electricity usage, after-hours consumption, and hidden waste. The system helps monitor these patterns in a simple and explainable way.")
    st.subheader("Project Objective")
    st.write("To identify unusual electricity consumption, generate alerts, and present results in a simple dashboard for decision-makers.")
    st.subheader("Technologies")
    st.write("Python, NumPy, Pandas, Matplotlib, Scikit-learn, Isolation Forest, and Streamlit.")
    st.subheader("How the AI Works")
    st.write("Isolation Forest learns the usual electricity patterns and flags records that look very different from the normal trend.")
    st.subheader("Limitations")
    st.write("This is synthetic data and does not confirm an electrical fault. It can only flag unusual consumption patterns for inspection.")
    st.subheader("Future Improvements")
    st.write("Smart meters, cost estimation, real-time monitoring, and mobile alerts can extend the project in the future.")


def main():
    """Main application entry point."""
    ensure_project_files()

    try:
        df = load_processed_data()
    except Exception as exc:
        st.error("⚠️ Dataset could not be loaded. Please check the data file.")
        st.write(str(exc))
        return

    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        [
            "Dashboard",
            "Consumption Analysis",
            "AI Anomaly Detection",
            "Building Analysis",
            "Alerts & Recommendations",
            "Data Explorer",
            "About Project",
        ],
    )

    if page == "Dashboard":
        show_dashboard(df)
    elif page == "Consumption Analysis":
        show_consumption_analysis(df)
    elif page == "AI Anomaly Detection":
        show_anomaly_detection(df)
    elif page == "Building Analysis":
        show_building_analysis(df)
    elif page == "Alerts & Recommendations":
        show_alerts_page(df)
    elif page == "Data Explorer":
        show_data_explorer(df)
    else:
        show_about_page()


if __name__ == "__main__":
    main()
