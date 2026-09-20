import json #importing json module to work with JSON data
from kafka import KafkaConsumer #importing consumer class to consume messages from a kafka topic


consumer=KafkaConsumer(
    "system-metrics", 
    bootstrap_servers=["localhost:9092"], ##specifying the kafka broker address
    auto_offset_reset="earliest",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
    
)
print("---------Consumer Anamoly Detector Started-------------")

for message in consumer:
    data=message.value
    cpu=data.get("cpu_usage",0)
    service=data.get("service","unknown")
    
    if cpu>80:
        print(f"[ANAMOLY DETECTED] High CPU usage detected for service '{service}': {cpu}%")
    else:
        print(f"[NORMAL] CPU Usage for service '{service}': {cpu}%")
