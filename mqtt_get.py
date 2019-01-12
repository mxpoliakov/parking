import json
from paho.mqtt.client import Client


class MyMqttClient(Client):
    def __init__(self, params):
        super().__init__()
        self.username_pw_set(params['username'], params['password'])
        self.connect(params['server'], params['port'])
        self.subscribe(params['topic'], 0)

    def on_message(self, client, obj, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))


if __name__ == "__main__":

    with open("mqtt_info.json") as params:
        mqtt_info = json.load(params)

    client = MyMqttClient(mqtt_info)

    rc = 0
    while rc == 0:
        rc = client.loop()
