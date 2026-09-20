from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "server_metrics",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    group_id="aiops-monitor"
)

anomaly_count = 0

print("AIOps Monitoring System Started...\n")

for message in consumer:

    data = json.loads(message.value.decode("utf-8"))

    server = data["server_id"]
    cpu = data["cpu_usage"]
    memory = data["memory_usage"]

    print("Message received:", server, "| CPU:", str(cpu) + "%")
    print("Memory:", str(memory) + "%")

    if cpu > 80:
        print("ALERT: High CPU detected")
        anomaly_count += 1
    else:
        print("Normal")

    print()

print("Total anomalies detected:", anomaly_count)