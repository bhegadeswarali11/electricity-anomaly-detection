import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def plot_consumption_trend(df):
    """Line chart for daily consumption trend."""
    daily = df.groupby("Date")["Consumption_kWh"].sum().sort_index()
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(daily.index, daily.values, color="#2E86DE", linewidth=2)
    ax.set_title("Daily Electricity Consumption")
    ax.set_xlabel("Date")
    ax.set_ylabel("Consumption (kWh)")
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    fig.tight_layout()
    return fig


def plot_building_consumption(df):
    """Bar chart for building-wise total consumption."""
    building_total = df.groupby("Building")["Consumption_kWh"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(building_total.index, building_total.values, color="#1F9D8A")
    ax.set_title("Building-wise Total Consumption")
    ax.set_xlabel("Building")
    ax.set_ylabel("Consumption (kWh)")
    ax.grid(axis="y", alpha=0.25)
    plt.xticks(rotation=45)
    fig.tight_layout()
    return fig


def plot_hourly_consumption(df):
    """Line chart for hourly consumption pattern."""
    hourly = df.groupby("Hour")["Consumption_kWh"].mean().sort_index()
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(hourly.index, hourly.values, color="#F39C12", linewidth=2)
    ax.set_title("Average Hourly Consumption")
    ax.set_xlabel("Hour")
    ax.set_ylabel("Consumption (kWh)")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    return fig


def plot_consumption_distribution(df):
    """Histogram for electricity distribution."""
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(df["Consumption_kWh"], bins=25, color="#8E44AD", edgecolor="black")
    ax.set_title("Consumption Distribution")
    ax.set_xlabel("Consumption (kWh)")
    ax.set_ylabel("Frequency")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()
    return fig


def plot_occupancy_vs_consumption(df):
    """Scatter plot of occupancy versus consumption."""
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(df["Occupancy"], df["Consumption_kWh"], alpha=0.6, color="#27AE60")
    ax.set_title("Occupancy vs Consumption")
    ax.set_xlabel("Occupancy")
    ax.set_ylabel("Consumption (kWh)")
    ax.grid(True, alpha=0.2)
    fig.tight_layout()
    return fig


def plot_anomaly_distribution(df):
    """Box plot by AI status."""
    fig, ax = plt.subplots(figsize=(8, 5))
    data = [df[df["AI_Status"] == "Normal"]["Consumption_kWh"], df[df["AI_Status"] == "Anomaly"]["Consumption_kWh"]]
    ax.boxplot(data, tick_labels=["Normal", "Anomaly"], patch_artist=True)
    ax.set_title("Consumption Distribution by AI Status")
    ax.set_ylabel("Consumption (kWh)")
    fig.tight_layout()
    return fig


def plot_anomaly_timeline(df):
    """Timeline of anomalies over time."""
    anomaly_df = df[df["AI_Status"] == "Anomaly"].copy()
    fig, ax = plt.subplots(figsize=(10, 4))
    if anomaly_df.empty:
        ax.text(0.5, 0.5, "No anomalies detected", ha="center", va="center")
        ax.axis("off")
    else:
        anomaly_df["Date"] = pd.to_datetime(anomaly_df["Date"])
        anomaly_df = anomaly_df.groupby("Date").size()
        ax.plot(anomaly_df.index, anomaly_df.values, color="#E74C3C", marker="o")
        ax.set_title("Anomaly Timeline")
        ax.set_xlabel("Date")
        ax.set_ylabel("Anomaly Count")
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
    fig.tight_layout()
    return fig
