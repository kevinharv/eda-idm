from confluent_kafka import Consumer, KafkaError
import json
import os
import sys
import signal

conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'testgroup',
    'auto.offset.reset': 'smallest'
}

consumer = Consumer(conf)

def signal_handler(sig, frame):
    print('Stopping consumer...')
    consumer.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

consumer.subscribe(['users'])

while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            print('End of partition reached {0}/{1}'.format(msg.topic(), msg.partition()))
        elif msg.error():
            raise KafkaException(msg.error())
    else:
        # print(f'Received message: {msg.value().decode("utf-8")}')
        print(json.loads(msg.value().decode("utf-8"))["name"])

consumer.close()
