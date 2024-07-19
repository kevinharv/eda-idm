from confluent_kafka import Producer
from faker import Faker
import json

fake = Faker()

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

conf = {
    'bootstrap.servers': 'localhost:9092'
}

producer = Producer(conf)

for i in range(10):
    user = {
      "name": fake.name()  
    }
    producer.produce('users', key=str(i), value=json.dumps(user), callback=delivery_report)

producer.flush()