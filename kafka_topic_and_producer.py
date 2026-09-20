# # Start Kafka
# docker compose up -d

# # Create topic
# docker exec -it kafka /opt/kafka/bin/kafka-topics.sh --create --topic server_metrics --bootstrap-server localhost:9092

from kafka import KafkaProducer
import json

# Create Kafka Producer
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda x: json.dumps(x).encode("utf-8")
)

# Server metric messages
messages = [
    {"server_id": "server01", "cpu_usage": 82, "memory_usage": 65},
    {"server_id": "server02", "cpu_usage": 75, "memory_usage": 70},
    {"server_id": "server03", "cpu_usage": 91, "memory_usage": 80},
    {"server_id": "server04", "cpu_usage": 68, "memory_usage": 60},
    {"server_id": "server05", "cpu_usage": 88, "memory_usage": 72},
    {"server_id": "server06", "cpu_usage": 79, "memory_usage": 67},
    {"server_id": "server07", "cpu_usage": 95, "memory_usage": 85},
    {"server_id": "server08", "cpu_usage": 72, "memory_usage": 62},
    {"server_id": "server09", "cpu_usage": 84, "memory_usage": 69},
    {"server_id": "server10", "cpu_usage": 90, "memory_usage": 78}
]

# Send messages to Kafka topic
for message in messages:
    producer.send("server_metrics", message)
    print("Sent:", message)

# Ensure all messages are published
producer.flush()

print("\n10 server metric messages successfully published!")

# Close producer
producer.close()

