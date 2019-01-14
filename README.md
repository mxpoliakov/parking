# Parking Assistance

Parking assistance for Softserve parklot

## Getting Started

### Wrapper

`wrapper.py` contains `ParkingAssistant` class, that takes care of all processes related to image processing and predicting.
On the same level there is `config.json` file with configuration options, required for proper wrapper work.

Example of usage:
```
parking_assistant = ParkingAssistant('config.json')
parking_assistant.assist()
```

### Camera simulator

`ParkingAssistant` supposes that its source directory, defined in config is always being replenished with new photos.
For that, there is `Camera` class in `utils` package, that copies image files from one directory to another, simulating live camera work.

Example of usage:
```
cam = Camera('camera_config.json')
cam.start()
```

### Run with docker

```
docker build --tag=parking .
docker run -it parking
```
