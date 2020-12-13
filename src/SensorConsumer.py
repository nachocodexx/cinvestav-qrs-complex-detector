from confluent_kafka import Consumer
import simplejson as json
from QRSProducer import QRSProducer
from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError
from concurrent.futures.thread import ThreadPoolExecutor
from threading import Thread, currentThread


class SensorConsumer(object):
    def __init__(self, *args, **kwargs):
        self.logger = kwargs.get('logger')
        self.TOPIC = kwargs.get('TOPIC', 's00')
        self.producer = args[0]
        self.bootstrap_servers = kwargs.get('BOOTSTRAP_SERVERS')
        self.schema_registry_url = kwargs.get("SCHEMA_REGISTRY_URL")
        self.group_id = kwargs.get("GROUP_ID")
        self.auto_offset = kwargs.get("auto_offset", "latest")
        self.Q = kwargs.get("Q")
        self.MAX_WORKERS = kwargs.get("MAX_WORKERS")

        self.consumer = AvroConsumer({
            'bootstrap.servers': self.bootstrap_servers,
            'group.id': self.group_id,
            'auto.offset.reset': self.auto_offset,
            'schema.registry.url': self.schema_registry_url
        })

        self.qrs_detector = kwargs.get('qrs_detector')

    def produceMessage(self):
        isRunning = True
        while isRunning:
            value = self.Q.get()
            key = {'prefix': 'sid', 'sensorId': value['sensorId']}
            threadName = currentThread().getName()
            self.producer.produce(key, value)
            self.Q.task_done()
            print("Sent message to kafka [{}]".format(threadName))

    def start(self):
        self.consumer.subscribe([self.TOPIC])
        for i in range(self.MAX_WORKERS):
            Thread(name="Thread-{}".format(i),
                   daemon=True, target=self.produceMessage).start()

        with ThreadPoolExecutor(max_workers=self.MAX_WORKERS) as executor:
            while True:
                message = None
                try:
                    message = self.consumer.poll(10)
                    # Q.put(message)
                except SerializerError as e:
                    print(
                        "Message deserialization failed for {}: {}".format(message, e))
                    break

                if message is None:
                    continue
                elif message.error():
                    self.logger.error(
                        "Consumer error: {}".format(message.error()))
                else:
                    data = message.value()
                    sensor_id = data['sensorId']
                    value = executor.submit(
                        self.qrs_detector.run, sensor_id, data['measurement'], data['timestamp'])

        self.consumer.close()
