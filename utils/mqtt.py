from paho.mqtt.client import Client


class MqttSender(Client):
    def __init__(self, user_id, params):
        super().__init__(user_id)

        self.username_pw_set(params['username'], params['password'])
        self.connect(params['server'], params['port'])
        self.mqtt_topic = params['topic']

    def send(self, obj):
        self.publish(self.mqtt_topic, obj)
