from confluent_kafka import avro

key_schema = avro.loads("""
{
  "doc": "Sample schema to help you get started.",
  "fields": [
    {
      "doc": "",
      "name": "prefix",
      "type": "string"
    },
    {
      "doc": "",
      "name": "sensorId",
      "type": "string"
    }
  ],
  "name": "QRSComplexKey",
  "namespace": "com.cinvestav",
  "type": "record"
}
""")
