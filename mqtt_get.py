import json
from paho.mqtt.client import Client


client = Client()


def on_message(client, obj, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

# Assign event callback
client.on_message = on_message

with open("mqtt_info.json") as params:
    mqtt_info = json.load(params)

client.username_pw_set(mqtt_info['username'], mqtt_info['password'])
client.connect(mqtt_info['server'], mqtt_info['port'])
client.subscribe(mqtt_info['topic'], 0)

rc = 0
while rc == 0:
    rc = client.loop()
