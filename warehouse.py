import json
import paho.mqtt.client as mqtt

# JSON-Daten
json_data = {
    "content": [
        ["Carrier", "Carrier", "Carrier"],
        ["WHITE", "RED", "BLUE"],
        ["Carrier", "Carrier", "Carrier"]
    ],
    "states": ["Empty", "Carrier", "WHITE", "RED", "BLUE", "COLOR_UNKNOWN"],
    "__comment__": "First array = Column nearest to cb"
}

# MQTT Broker Einstellungen
mqtt_broker = "127.0.0.1"  # Beispiel-Broker, ersetze dies durch deine Broker-Adresse
mqtt_port = 1883
topic = "minifactory/right/fabric/Warehouse/Set"

# Funktion zum Senden einer Nachricht über MQTT
def send_json_data(client, topic, json_data):
    payload = json.dumps(json_data)
    client.publish(topic, payload=payload, qos=0, retain=False)

# Callback-Funktion bei Verbindungsaufbau
def on_connect(client, userdata, flags, rc):
    print("Verbindung erfolgreich. Verbindungscode:", rc)
    send_json_data(client, topic, json_data)
    client.disconnect()

# MQTT Verbindung aufbauen und Daten senden
client = mqtt.Client()
client.on_connect = on_connect

client.connect(mqtt_broker, mqtt_port, 60)

client.loop_forever()
