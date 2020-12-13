import json


class Measurement(object):
    def __init__(self, timestamp, value):
        self.timestamp = timestamp
        self.value = value

    def toJSON(self):
        return json.dumps(self.__dict__)
