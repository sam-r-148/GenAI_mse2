'''Problem Statement

You are working as an AIOps Engineer for an online university portal. The monitoring system has recorded the following server response times in milliseconds over 20 time intervals:

response_time = [
    120, 125, 118, 130, 122,
    127, 124, 121, 129, 126,
    123, 128, 125, 122, 131,
    700, 127, 119, 650, 124
]

Most of the requests have a response time between approximately 118-131 ms, but some values appear significantly different.

Your task is to build a Python-based anomaly detection system using Isolation Forest.'''

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest


def detect_anomalies():
    # 1. Dataset definition
    response_time = [
        120, 125, 118, 130, 122,
        127, 124, 121, 129, 126,
        123, 128, 125, 122, 131,
        700, 127, 119, 650, 124
    ]

    # 2. Reshape data into 2D array format required by Scikit-Learn
    X = np.array(response_time).reshape(-1, 1)

    # Contamination is set to 0.1 (10%), as 2 out of 20 points are clear outliers (700 and 650)
    model = IsolationForest(contamination=0.1, random_state=42)

    # 4. Fit model and predict anomaly status (1: Normal/Inlier, -1: Anomaly/Outlier)
    model.fit(X)
    predictions = model.predict(X)
    scores = model.decision_function(X)  # Lower scores indicate higher anomaly severity

    # 5. Build structured DataFrame for report visualization
    df = pd.DataFrame({
        'Interval_Index': range(1, len(response_time) + 1),
        'Response_Time_ms': response_time,
        'Anomaly_Score': np.round(scores, 4),
        'Prediction': predictions,
        'Status': ['Anomaly' if p == -1 else 'Normal' for p in predictions]
    })

    print("=" * 65)
    print("      AIOPS ANOMALY DETECTION SYSTEM (ISOLATION FOREST)")
    print("=" * 65)
    print("\nSummary of Scanned Telemetry:")
    print(f"Total Intervals: {len(df)}")
    print(f"Normal Count   : {(df['Prediction'] == 1).sum()}")
    print(f"Anomaly Count  : {(df['Prediction'] == -1).sum()}")
    print("-" * 65)

    print("\nFull Data Log:")
    print(df.to_string(index=False))

    print("\n" + "=" * 65)
    print("DETECTED ANOMALIES:")
    print("-" * 65)
    anomalies = df[df['Prediction'] == -1]
    for idx, row in anomalies.iterrows():
        print(f"  Interval {int(row['Interval_Index'])}: Response Time = {int(row['Response_Time_ms'])} ms (Anomaly Score: {row['Anomaly_Score']})")
    print("=" * 65)

    return df


if __name__ == "__main__":
    detect_anomalies()

