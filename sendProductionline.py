import paho.mqtt.client as mqtt
import json

broker_address = "127.0.0.1"
broker_port = 1883

side = "right"
part = "fabric"
product = "product"

topicsend = f"minifactory/{side}/{part}/{product}"
topicreceive = "minifactory/#"

name = "Main1"
run = True
start_at = "START"
end_at = "END"
with_oven = True
with_saw = True
with_PM = False
with_WH = False
color = "White"

data = {
    "name": name,
    "run": run,
    "start_at": start_at,
    "end_at": end_at,
    "with_oven": with_oven,
    "with_saw": with_saw,
    "with_PM": with_PM,
    "with_WH": with_WH,
    "color": color
}

payload = json.dumps(data)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topicreceive)

def on_message(client, userdata, msg):
    received_topic = msg.topic
    received_payload = msg.payload.decode("utf-8")

    print(f"Received message on topic {received_topic}: {received_payload}")

    if "minifactory/right/fabric/producttest" in received_topic:
        print("Message received on the product topic on the right side.")

        received_data = json.loads(received_payload)
        name = received_data["name"]
        with_oven = received_data["with_Caramel"]
        with_saw = received_data["with_Flakes"]
        with_PM = received_data["with_Lid"]
        color = received_data["color"]

        print(f"Name: {name}, Oven: {with_oven}, Saw: {with_saw}, PM: {with_PM}, Color: {color}")

        data = {
            "name": name,
            "run": run,
            "start_at": start_at,
            "end_at": end_at,
            "with_oven": with_oven,
            "with_saw": with_saw,
            "with_PM": with_PM,
            "with_WH": with_WH,
            "color": color
        }

        payload = json.dumps(data)
        print(f"{payload}")
        client.publish(topicsend, payload)

    elif "minifactory/left" in received_topic:
        print("Message received on the left side topic.")

    else:
        print("Message received on an unknown topic.")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_address, broker_port, 60)
client.loop_start()  # Hier wird loop_start() verwendet, um die Schleife im Hintergrund laufen zu lassen

# Hier könntest du deinen anderen Code einfügen, der neben der Schleife ausgeführt wird

# Beispiel: Warte auf Benutzereingabe, um das Programm zu stoppen
while True:
    user_input = input("Drücke 'q' und Enter, um das Programm zu beenden: ")
    if user_input.lower() == 'q':
        break

# Programm beenden
client.loop_stop()
client.disconnect()
print("Programm beendet.")
