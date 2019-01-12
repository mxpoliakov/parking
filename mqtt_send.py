import json
from paho.mqtt.client import Client


predictions = {"test": False, 0: True, 1: False, 2: False, 3: False}
with open("mqtt_info.json") as params:
    mqtt_info = json.load(params)

client = Client()
client.username_pw_set(mqtt_info['username'], mqtt_info['password'])
client.connect(mqtt_info['server'], mqtt_info['port'])
client.publish(mqtt_info['topic'], json.dumps(predictions))