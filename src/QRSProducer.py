from confluent_kafka import Producer
from confluent_kafka.avro import AvroProducer
import logging
from schemas.key_schema import key_schema
from schemas.value_schema import value_schema


class QRSProducer(object):
    def __init__(self, **kwargs):
        self.TOPIC = kwargs.get("TOPIC", "db")
        self.schema_registry_url = kwargs.get("SCHEMA_REGISTRY_URL")
        self.logger = kwargs.get("logger", logging.getLogger())
        self.Q = kwargs.get("Q")

        self.bootstrap_servers = kwargs.get("BOOTSTRAP_SERVERS")

        self.producer = AvroProducer({
            'bootstrap.servers': self.bootstrap_servers,
            'on_delivery': self.delivery_report,
            'schema.registry.url': self.schema_registry_url
        }, default_key_schema=key_schema, default_value_schema=value_schema)

    def delivery_report(self, error, message):
        """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
        if error is not None:
            print('Message delivery failed: {}'.format(error))
        else:
            print('Message delivered to {} [{}]'.format(
                message.topic(), message.partition()))

    def produce(self, key, value):
        self.producer.produce(topic=self.TOPIC, value=value, key=key)
        self.producer.flush()
