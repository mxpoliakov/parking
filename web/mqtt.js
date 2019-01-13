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
	let json = JSON.parse(message.payloadString);
	document.querySelector('.time').innerHTML = json.metadata.processing_start_time;
	Object.keys(json.parking_places).forEach(function(key) {
		document.querySelector('.pl_' + key.toString()).classList.remove('free');
		if (json.parking_places[key]) {
			document.querySelector('.pl_' + key.toString()).classList.add('free');
		}
	});
}
