import numpy as np
import simplejson as json
from utils.Timer import TimerUtils


class QRSResult(object):
    def __init__(self, **kwargs):
        self.sensorId = kwargs.get("sensorId", "FAKE-ID")
        self.measurement = kwargs.get('measurement', .0)
        self.filtered_ecg = kwargs.get(
            "filtered_ecg", complex(0, 0)).real
        # print(self.f)
        self.differentiated_ecg = kwargs.get(
            "differentiated_ecg", complex(0, 0)).real
        self.squared_ecg = kwargs.get(
            "squared_ecg", complex(0, 0)).real
        self.integrated_ecg = kwargs.get(
            "integrated_ecg", complex(0, 0)).real
        self.timestamp = kwargs.get("timestamp", 0)
        self.qrs_timestamp = TimerUtils.currentTime()

    # def toJSON(self):
    #     sensorId = self.__dict__['sensorId'][0]
    #     d = {**self.__dict__}
    #     del d['sensorId']
    #     newD = {**{'sensorId': sensorId}, **d}
    #     return json.dumps(newD)
    def toDict(self):
        return self.__dict__

    def __str__(self):
        return 'QRSResult({},{},{},{})'.format(
            self.measurement, self.filtered_ecg, self.differentiated_ecg, self.squared_ecg, self.integrated_ecg)
