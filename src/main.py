import asyncio
from SensorConsumer import SensorConsumer
from QRSProducer import QRSProducer
import os
import logging
import sys
import redis
from QRSDetectorOnline import QRSDetectorOnline
import queue


logging.basicConfig(filename="app.log", format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)


async def main():
    # ___________________QUEUE____________________________
    Q = queue.Queue(200)
    MAX_WORKERS = os.getenv("MAX_WORKERS", 100)
    # ______________________________________________________

    # Redis = redis.Redis(host="localhost", port="6379", db=0)
    Redis = redis.Redis(
        host="ec2-54-162-119-149.compute-1.amazonaws.com", port="6379", db=0)

    # ______________________________________________________
    logger = logging.getLogger()
    # sensor_id = os.getenv("SENSOR_ID", "7dd77f33-a86e-43dc-9e3d-264a6e119f0e")
    CONSUMER_TOPIC = os.getenv('CONSUMER_TOPIC', "s00")
    PRODUCER_TOPIC = os.getenv('PRODUCER_TOPIC', "db")
    SCHEMA_REGISTRY_URL = os.getenv(
        'SCHEMA_REGISTRY_URL', "http://ec2-3-90-166-46.compute-1.amazonaws.com:8081")

    BOOTSTRAP_SERVERS = os.getenv(
        'BOOTSTRAP_SERVERS', 'ec2-3-90-166-46.compute-1.amazonaws.com:9092,ec2-54-91-17-192.compute-1.amazonaws.com:9093')
    GROUP_ID = os.getenv('GROUP_ID', "g1")
    # ________________________________________________________
    logger.info('[ QRS COMPLEX DETECTOR ]')
    # ________________________________________________________

    qrs_detector = QRSDetectorOnline(redis=Redis, Q=Q)

    # ______________________________________________________
    qrs_producer = QRSProducer(
        TOPIC=PRODUCER_TOPIC,
        BOOTSTRAP_SERVERS=BOOTSTRAP_SERVERS,
        SCHEMA_REGISTRY_URL=SCHEMA_REGISTRY_URL,
        logger=logger,
        Q=Q
    )

    sc = SensorConsumer(
        qrs_producer,
        qrs_detector=qrs_detector,
        BOOTSTRAP_SERVERS=BOOTSTRAP_SERVERS,
        TOPIC=CONSUMER_TOPIC,
        GROUP_ID=GROUP_ID,
        SCHEMA_REGISTRY_URL=SCHEMA_REGISTRY_URL,
        logger=logger,
        Q=Q,
        MAX_WORKERS=MAX_WORKERS
    )
    # ______________________________________________________
    sc.start()

if __name__ == "__main__":
    asyncio.run(main())
