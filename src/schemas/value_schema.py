from confluent_kafka import avro

value_schema = avro.loads("""
{
  "doc": "QRS Complex result",
  "fields": [
    {
      "doc": "",
      "name": "sensorId",
      "type": "string"
    },
    {
      "doc": "",
      "name": "measurement",
      "type": "double"
    },
    {
      "doc": "",
      "name": "filtered_ecg",
      "type": "double"
    },
    {
      "doc": "",
      "name": "differentiated_ecg",
      "type": "double"
    },
    {
      "doc": "",
      "name": "squared_ecg",
      "type": "double"
    },
    {
      "doc": "",
      "name": "integrated_ecg",
      "type": "double"
    },
    {
      "doc": "",
      "name": "timestamp",
      "type": "long"
    },
    {
      "doc": "",
      "name": "qrs_timestamp",
      "type": "long"
    }
  ],
  "name": "QRSComplexResult",
  "namespace": "com.cinvestav",
  "type": "record"
}
""")
