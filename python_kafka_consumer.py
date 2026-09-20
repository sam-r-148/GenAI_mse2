from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    "server_metrics",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    group_id="server-monitor"
)

print("Kafka Consumer started...")
print("Waiting for server metrics...\n")

for message in consumer:
    data = json.loads(message.value.decode("utf-8"))

    server = data["server_id"]
    cpu = data["cpu_usage"]
    memory = data["memory_usage"]

    print("Received:")
    print("Server:", server)
    print("CPU:", str(cpu) + "%")
    print("Memory:", str(memory) + "%")

    if cpu > 80:
        print("\nALERT: High CPU detected on", server)

    print()