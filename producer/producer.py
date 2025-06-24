import json
import random
import signal
import sys
import logging
import os
import time
from faker import Faker
from confluent_kafka import Producer

fake = Faker()

logging.basicConfig(level = logging.INFO , format ="%(asctime)s - %(levelname)s -%(message)s")
logger = logging.getLogger(__name__)

KAFKA_BROKER = os.getenv("KAFKA_BROKER" , "localhost:9092")
TOPIC_NAME = os.getenv("TOPIC_NAME" , "orders")

if not KAFKA_BROKER:
    raise ValueError("KAFKA_BROKER environment variable is not set.")

kafka_config = {
    'bootstrap.servers': KAFKA_BROKER
}
producer = Producer(kafka_config)

def generate_order_event():
    return {
        "order_id": fake.uuid4(),
        "user_id": fake.uuid4(),
        "order_time": fake.iso8601(),
        "session_id": fake.uuid4(),
        "items": [
            {
                "item_id": fake.uuid4(),
                "product_name": fake.word(),
                "quantity": random.randint(1, 5),
                "price": round(random.uniform(10, 500), 2)
            }
            for _ in range(random.randint(1, 3))
        ],
        "total_amount": round(random.uniform(20, 1500), 2),
        "payment_method": fake.random_element(("credit_card", "paypal", "bank_transfer")),
        "url": fake.uri_path(),
        "shipping_address": fake.address(),
        "order_status": fake.random_element(("placed", "shipped", "delivered", "cancelled"))
    }

def delivery_reporter(err, msg):
    if err:
        logger.error(f'Message Delivery failed with {err}')
    else :
        logger.info(f'Message Delivered to {msg.topic()} [{msg.partition()}]')

def shutdown_handler(sig , frame):
    logger.info("Shutting down producer ...")
    producer.flush()
    sys.exit(0)

signal.signal(signal.SIGINT , shutdown_handler)
signal.signal(signal.SIGTERM , shutdown_handler)

def main():
    while True:
        try:
            event = generate_order_event()
            key = event["session_id"]
            value = json.dumps(event)

            producer.produce(topic = TOPIC_NAME , key= key , value = value , callback = delivery_reporter)
            producer.poll(0)
            logger.info(json.dumps(event, indent=2))
            time.sleep(1)

        except BufferError as e :
            logger.warning(f"Buffer is full, waiting :{e}")
            time.sleep(0.5)
        except Exception as e:
            logger.error(f'Unexpected error : {e}')
            time.sleep(1)

if __name__ == "__main__":
    main()