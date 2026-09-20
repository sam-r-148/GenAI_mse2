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

import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

response_time = [
    120, 125, 118, 130, 122,
    127, 124, 121, 129, 126,
    123, 128, 125, 122, 131,
    700, 127, 119, 650, 124
]

input = [[n] for n in response_time]

model = IsolationForest(contamination=0.1,random_state=42)

model.fit(input)

pred = model.predict(input)

print(pred)


plt.plot(input)

# plt.figure(figsize=(10,5))
# plt.scatter(range(1, len(response_time)+1), response_time,
#             c=["red" if p == -1 else "blue" for p in pred],
#             s=80, marker="o")

# plt.title("Response Time Anomaly Detection")
# plt.xlabel("Interval")
# plt.ylabel("Response Time (ms)")
# plt.legend(["Normal","Anomaly"], loc="upper left")
# plt.show()