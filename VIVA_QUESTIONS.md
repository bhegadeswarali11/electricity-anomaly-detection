# Viva Questions and Answers

## Basic
### 1. What is the objective of your project?
The objective is to analyze electricity consumption in a college and detect unusual patterns using AI.

### 2. Why did you choose electricity consumption?
Because electricity usage is an important real-world resource and can show abnormal patterns that need attention.

### 3. What problem does the system solve?
It helps identify unusual energy usage and possible wastage without physically inspecting the equipment.

### 4. What technologies did you use?
We used Python, NumPy, Pandas, Matplotlib, Scikit-learn, Isolation Forest, and Streamlit.

## AI
### 5. What is Artificial Intelligence?
Artificial Intelligence is the ability of a system to perform tasks that normally require human intelligence.

### 6. What is Machine Learning?
Machine Learning is a branch of AI that allows computers to learn from data instead of being explicitly programmed for every rule.

### 7. What is anomaly detection?
Anomaly detection is the process of finding data points that are very different from normal patterns.

### 8. What is Isolation Forest?
Isolation Forest is an unsupervised machine learning algorithm used to detect anomalies by isolating unusual data points.

### 9. Why did you use Isolation Forest?
It is simple, effective for anomaly detection, and suitable for a beginner-friendly project.

### 10. Is Isolation Forest supervised or unsupervised?
It is unsupervised because it does not need manually labelled normal and anomaly data.

### 11. What is contamination?
Contamination is the expected fraction of anomalies in the dataset.

### 12. What is an anomaly?
An anomaly is an unusual observation that differs significantly from the normal pattern.

### 13. How does the model identify unusual records?
It learns the usual pattern in the dataset and marks points that are very different from that pattern as anomalies.

## Data
### 14. How did you generate the dataset?
The project creates a synthetic dataset using random distributions and realistic consumption patterns for different buildings and times.

### 15. Why did you use synthetic data?
Because we do not have a real college electricity dataset in the project, so a realistic synthetic dataset helps demonstrate the system clearly.

### 16. What features are used?
The main features include consumption, occupancy, temperature, hour, working hours, and previous consumption.

### 17. How did you handle missing values?
We used Pandas functions like fillna and numeric conversion to handle missing values.

### 18. Why is preprocessing required?
Preprocessing removes errors, standardizes values, and improves model performance and analysis quality.

## Python
### 19. Why did you use NumPy?
NumPy is useful for efficient numerical calculations and array-based operations.

### 20. Why did you use Pandas?
Pandas helps in reading, cleaning, transforming, and analyzing tabular data.

### 21. Why did you use Matplotlib?
Matplotlib is used to create useful visualizations such as charts and graphs.

### 22. Why did you use Streamlit?
Streamlit is used to build an interactive dashboard quickly and easily.

## Limitations
### 23. Can the system confirm an electrical fault?
No, the system does not physically inspect equipment and cannot confirm a fault.

### 24. What happens if the data is incorrect?
The AI results may be less accurate, so data cleaning and validation are important.

### 25. What would you do to make this a real-world system?
We would use smart meters, a live data source, more accurate historical data, and stronger monitoring infrastructure.

### 26. What is the role of the dashboard?
The dashboard presents charts, KPI cards, and alerts so users can understand electricity usage quickly.

### 27. Why is the project useful for a college?
It helps students understand electricity monitoring, data analysis, and AI in a practical application.

### 28. What is the difference between normal and anomaly records?
Normal records follow the expected pattern, while anomaly records are unusually high or different compared to normal behavior.

### 29. Can the system identify the exact cause of unusual consumption?
No. It can only identify unusual patterns and suggest inspection.

### 30. What is the purpose of alerts?
Alerts help users quickly identify abnormal situations for review.

### 31. Why is the project considered AI-based?
Because it uses machine learning to detect outliers and abnormal patterns in electricity consumption data.

### 32. What is the benefit of using a dashboard?
A dashboard makes the data easy to understand and helps present results clearly to users.

### 33. Why not use deep learning?
Deep learning is not necessary for this simple project, and the goal is to keep it beginner-friendly and explainable.

### 34. What is the meaning of unusual consumption?
It means the record is significantly different from the usual pattern for that building or time period.

### 35. What are the important project limitations to mention in viva?
The dataset is synthetic, the system analyzes consumption data only, and it cannot physically confirm faults or exact appliance issues.
