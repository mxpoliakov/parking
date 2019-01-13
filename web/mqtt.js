const client = new Paho.MQTT.Client('m24.cloudmqtt.com', 39931, 'receiver');
client.onMessageArrived = onMessageArrive;
client.connect({
	useSSL: true,
	userName: 'cijtmtir',
	password: 'O2t08bkdacPa',
	onSuccess: onConnect
});

function onConnect() {
	client.subscribe('parking');
}

function onMessageArrive(message) {
	console.log('1');
	let json = JSON.parse(message.payloadString);
	console.log('2');
	console.log(json);
}
