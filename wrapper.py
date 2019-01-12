from model import Model
from cropper import Cropper
import json
from time import time, localtime, strftime

from mqtt_send import MqttSender


class ParkingAssistant(object):

    def __init__(self, config):
        self.cropper = Cropper(config, Model('model.h5'))

        with open("mqtt_info.json") as params:
            mqtt_info = json.load(params)

        self.mqtt = MqttSender("sender", mqtt_info)

        self.predictions = None

    def predict(self, image):
        self.predictions = self.cropper.predict(image)

        return self.predictions

    def analyze(self, image):

        splited = image.split("/")
        image_name = splited[-1]
        dir_name = "/".join(splited[:-1])

        result = {}
        start_time = time()
        predicts = self.predict(image)
        processing_time = round(time() - start_time, 2)
        result["parking_places"] = predicts

        free = len(list(filter(lambda x: x, predicts.values())))
        occupied = len(list(filter(lambda x: not x, predicts.values())))

        result["parking"] = {"free": free, "occupied": occupied}
        result["metadata"] = {"source_folder": dir_name,
                              "source_file": image_name,
                              "processing_time": processing_time,
                              "processing_start_time": strftime('%Y-%m-%d %H:%M:%S', localtime(start_time))}
        print(result)
        self.mqtt.send(json.dumps(result))


pa = ParkingAssistant('mapping.json')
pa.analyze('images/2018-07-16 10_06_58.325.jpg')
