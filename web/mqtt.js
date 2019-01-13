const client = new Paho.MQTT.Client('<server>', 10000, 'receiver');
client.onMessageArrived = onMessageArrive;
client.connect({
    useSSL: true,
    userName: '<username>',
    password: '<password>',
    onSuccess: onConnect
});

function onConnect(){
    client.subscribe('parking');
}

function onMessageArrive(message) {
    console.log('1');
    JSON.parse(message.payloadString);
    console.log('2')
}
