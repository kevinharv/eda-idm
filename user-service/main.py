from confluent_kafka import Producer

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

conf = {
    'bootstrap.servers': 'localhost:9092'
}

producer = Producer(conf)

for i in range(1000):
    producer.produce('test_topic', key=str(i), value=f'Hello Kafka {i}', callback=delivery_report)

producer.flush()
