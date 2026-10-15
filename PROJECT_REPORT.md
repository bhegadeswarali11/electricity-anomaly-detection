# AI-Based College Electricity Consumption & Anomaly Detection System

## 1. Title
AI-Based College Electricity Consumption & Anomaly Detection System

## 2. Abstract
This project develops a simple and explainable AI-based system to monitor electricity consumption in different college buildings. It uses historical data, data preprocessing, and the Isolation Forest machine learning model to detect unusual electricity usage patterns. The system presents the results in a Streamlit dashboard with charts and alerts.

## 3. Introduction
College campuses consume electricity across classrooms, laboratories, hostels, libraries, and other departments. Sometimes electricity usage is higher than usual due to non-working hours, holidays, or abnormal operational patterns. This project helps identify such unusual patterns in an easy-to-understand way.

## 4. Problem Statement
Manual monitoring of college electricity usage is difficult. High consumption may go unnoticed, especially during after-hours or holidays. There is a need for a simple system that can analyze energy usage and detect abnormal patterns.

## 5. Motivation
The project combines real-world energy awareness with beginner-friendly artificial intelligence. It helps students understand data science, machine learning, and dashboard development in a practical setting.

## 6. Objectives
- Analyze electricity consumption in different college buildings
- Detect abnormal usage patterns
- Use AI to find unusual records
- Present alerts and recommendations
- Build a simple and professional dashboard

## 7. Existing System
Most college energy monitoring is manual or based on simple spreadsheets. These methods usually do not detect unusual patterns automatically.

## 8. Proposed System
A Python-based system is proposed that uses synthetic yet realistic data, cleans it, analyzes it, and detects anomalies using Isolation Forest. The solution is displayed in a Streamlit dashboard.

## 9. System Architecture
Electricity Data -> Data Collection -> Data Cleaning -> Feature Engineering -> Data Analysis -> Isolation Forest -> Normal / Anomaly -> Alert System -> Streamlit Dashboard.

## 10. Technologies Used
Python, NumPy, Pandas, Matplotlib, Scikit-learn, Isolation Forest, and Streamlit.

## 11. Dataset Description
The project uses a synthetic dataset containing records such as Record ID, date, time, building, consumption, occupancy, temperature, weekday, day type, working hours, and previous consumption.

## 12. Data Preprocessing
The dataset is cleaned by removing duplicates, handling missing values, converting date and time values, fixing numeric fields, and filtering invalid records.

## 13. Feature Engineering
Useful features such as hourly consumption, occupancy, temperature, working hours, and previous consumption are used to help the AI model understand normal patterns.

## 14. AI Methodology
The model learns from the available dataset without needing manually labelled normal and abnormal examples. It identifies values that differ strongly from the usual pattern.

## 15. Isolation Forest
Isolation Forest is an unsupervised anomaly detection algorithm. It randomly isolates observations and marks those that are easiest to isolate as anomalies.

## 16. Anomaly Detection
The model labels records as Normal or Anomaly based on how different they are from the usual pattern. These records are then shown in charts and alerts.

## 17. Alert Generation
Alerts are generated based on unusual consumption, after-hours usage, weekend patterns, or sudden spikes. The alert system shows the building, time, consumption, reason, and recommendation.

## 18. Dashboard
The dashboard uses Streamlit to display KPI cards, charts, filtering options, and project insights in a professional college-style layout.

## 19. Results
The system successfully generates a dataset, detects anomalies, and visualizes the results. The dashboard helps users understand where electricity usage is irregular and which buildings need inspection.

## 20. Limitations
The dataset is synthetic, and the system does not physically inspect equipment. It identifies unusual trends, not exact faults.

## 21. Future Scope
Future work may include smart meter integration, cost estimation, real-time monitoring, and mobile notifications.

## 22. Conclusion
This project is a practical implementation of AI in electricity monitoring. It gives students the chance to understand data handling, anomaly detection, and dashboard creation in a simple and effective way.

## 23. References
- Scikit-learn documentation
- Pandas documentation
- Matplotlib documentation
- Streamlit documentation
- Foundation of AI course materials
