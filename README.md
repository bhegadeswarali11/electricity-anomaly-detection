# AI-Based College Electricity Consumption & Anomaly Detection System

## Description
This project is a beginner-friendly AI mini-project for a college assignment. It analyzes electricity usage across different college buildings and uses an Isolation Forest model to detect unusual consumption patterns. The system is designed to support campus energy monitoring and highlight possible wastage without claiming that a real electrical fault is confirmed.

## Features
- Synthetic electricity dataset generation
- Data cleaning with Pandas
- NumPy-based statistical analysis
- Isolation Forest anomaly detection
- Streamlit dashboard
- Building-wise and daily consumption analysis
- AI alerts and recommendations
- CSV export and filtering

## Technologies
- Python
- NumPy
- Pandas
- Matplotlib
- Scikit-learn
- Streamlit

## AI Model
The system uses Isolation Forest, which is an unsupervised machine learning algorithm. It learns the normal pattern of electricity consumption and flags records that are very different from this typical behavior.

## Installation
```bash
pip install -r requirements.txt
```

## Run
```bash
streamlit run app.py
```

The project is also configured for VS Code. Open the project folder, select the Python environment, and click the Run button. The app automatically checks for the dataset, creates missing folders, generates the CSV if needed, cleans the data, runs the AI model, and opens the dashboard.

## Project Structure
- app.py — main Streamlit interface
- generate_data.py — synthetic dataset generator
- data_loader.py — loads the dataset
- data_processing.py — cleaning and preprocessing
- analytics.py — statistics and building analysis
- anomaly_detection.py — AI model logic
- visualization.py — charts and graphs
- alerts.py — alert generation
- config.py — configuration constants
- data/electricity_consumption.csv — dataset
- outputs/processed_electricity_data.csv — processed data
- .vscode/launch.json — VS Code run configuration

## Dataset
The project creates a realistic synthetic dataset with records for different campus buildings, hours, occupancy, temperature, day type, and previous consumption values. No internet download is required.

## AI Workflow
Electricity Data -> Data Cleaning -> Feature Preparation -> Isolation Forest -> Anomaly Detection -> Alerts -> Dashboard

## Limitations
- The dataset is synthetic.
- The system analyzes data, not physical electrical hardware.
- An anomaly does not confirm a real electrical fault.
- It cannot identify the exact appliance causing abnormal usage.

## Future Scope
- Real-time smart meter integration
- Building management system integration
- Appliance-level monitoring
- Cost estimation and recommendations
- Mobile alert system
