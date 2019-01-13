from utils.model import Model
from utils.cropper import Cropper
import json
from time import time, localtime, strftime
import glob
import os
import threading

from utils.mqtt import MqttSender


class ParkingAssistant(object):

    def __init__(self, config_file):

        config = json.loads(open(config_file).read())

        self.cropper = Cropper(config['parking_map'], Model('model.h5'))

        self.mqtt = MqttSender("sender", config['mqtt'])

        self.predictions = None
        self.take_next = False
        self.thread = None

        self.delay = config['delay']
        self.last_take_time = time()-self.delay
        self.dir_name = config['source_directory']

    def predict(self, image):
        self.predictions = self.cropper.predict(image)

        return self.predictions

    def analyze(self, image):

        splited = image.split("/")[-1].split("\\")
        image_name = splited[-1]

        result = {}
        start_time = time()
        predicts = self.predict(image)
        processing_time = round(time() - start_time, 2)
        result["parking_places"] = predicts

        free = len(list(filter(lambda x: x, predicts.values())))
        occupied = len(list(filter(lambda x: not x, predicts.values())))

        result["parking"] = {"free": free, "occupied": occupied}
        result["metadata"] = {"source_folder": self.dir_name,
                              "source_file": image_name,
                              "processing_time": processing_time,
                              "processing_start_time": strftime('%Y-%m-%d %H:%M:%S', localtime(start_time))}

        self.mqtt.send(json.dumps(result))

    def check_to_take_next(self):
        while True:
            if time() - self.last_take_time >= self.delay:
                self.take_next = True

    def analyzer(self):
        last_file = None
        while True:
            if not self.take_next: continue
            self.take_next = False
            self.last_take_time = time()

            list_of_files = glob.glob('{}/*.jpg'.format(self.dir_name))  # * means all if need specific format then *.csv
            try:
                latest_file_in_dir = max(list_of_files, key=os.path.getctime)
            except ValueError as e:
                print("no file")
                continue
            file_name = latest_file_in_dir.split("\\")[-1]
            if last_file == file_name:
                print("no new file")
                continue
            last_file = file_name

            self.analyze(latest_file_in_dir)

    def assist(self):
        print("Start parking assistance")
        self.thread = threading.Thread(target=self.check_to_take_next)
        self.thread.start()
        self.analyzer()


if __name__ == "__main__":
    pa = ParkingAssistant('config.json')
    pa.assist()
