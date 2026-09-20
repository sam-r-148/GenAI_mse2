import pandas as pd
import matplotlib.pyplot as plt

# Create sample dataset

data = {
    "Timestamp": [
        "10:00", "10:01", "10:02", "10:03", "10:04",
        "10:05", "10:06", "10:07", "10:08", "10:09",
        "10:10", "10:11", "10:12", "10:13", "10:14",
        "10:15", "10:16", "10:17", "10:18", "10:19"
    ],

    "CPU": [
        45, 52, 48, 55, 50,
        95, 51, 49, 54, 53,
        47, 50, 97, 52, 48,
        51, 55, 49, 92, 53
    ],

    "Memory": [
        60, 62, 61, 63, 60,
        64, 62, 61, 63, 62,
        61, 64, 65, 62, 61,
        63, 62, 64, 65, 63
    ],

    "Response_Time": [
        120, 125, 118, 130, 122,
        135, 128, 124, 126, 121,
        123, 127, 140, 125, 122,
        129, 124, 128, 145, 126
    ]
}

df = pd.DataFrame(data)


# Total records

print("Total records:", len(df))


# Basic statistics

print("\nBasic Statistics:")

print("\nCPU Usage")
print("Mean:", df["CPU"].mean())
print("Minimum:", df["CPU"].min())
print("Maximum:", df["CPU"].max())

print("\nMemory Usage")
print("Mean:", df["Memory"].mean())
print("Minimum:", df["Memory"].min())
print("Maximum:", df["Memory"].max())

print("\nResponse Time")
print("Mean:", df["Response_Time"].mean())
print("Minimum:", df["Response_Time"].min())
print("Maximum:", df["Response_Time"].max())


# Threshold-based anomaly detection

cpu_threshold = 90

anomalies = []

for i in range(len(df)):

    if df.loc[i, "CPU"] > cpu_threshold:
        anomalies.append(i)


# Print anomalies

print("\nAnomalies detected:", len(anomalies))

print("\nTimestamp\tCPU\tStatus")

for i in anomalies:

    print(
        df.loc[i, "Timestamp"],
        "\t\t",
        str(df.loc[i, "CPU"]) + "%",
        "\tANOMALY"
    )


# Display graph

plt.figure(figsize=(10, 5))

plt.plot(
    df["Timestamp"],
    df["CPU"],
    marker="o",
    label="CPU Usage"
)

# Mark anomalies

for i in anomalies:

    plt.scatter(
        df.loc[i, "Timestamp"],
        df.loc[i, "CPU"],
        marker="x",
        s=100
    )

# Show threshold

plt.axhline(
    y=cpu_threshold,
    linestyle="--",
    label="Anomaly Threshold"
)

plt.xlabel("Timestamp")
plt.ylabel("CPU Usage (%)")
plt.title("AIOps Log Anomaly Detection")

plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()

plt.show()