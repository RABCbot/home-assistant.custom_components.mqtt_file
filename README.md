# Home-Assistant-MQTT-file
Custom MQTT sensor, subscribe to a topic and save the Base64 payload to a file

## Installation
Copy all the files from this repo, to your custom_component folder

## Configuration
Add to your configuration yaml:
```yaml
sensor:
- platform: mqtt_file
  topic: butler/announce
  filename: /share/audio.wav
```

