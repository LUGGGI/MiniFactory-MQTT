import paho.mqtt.client as mqtt
import json

# MQTT Broker Konfiguration
broker_address = "127.0.0.1"
port = 1883
#Topic zum versenden von Nachrichten
topic = "minifactory/right/fabric/producttest"

# Standardwerte für das Produkt
name = "Test"
with_Caramel = False
with_Flakes = False
with_Lid = False
color = "WHITE"

# Produktinformationen als JSON-Payload
data = {
    "name": name,
    "with_Caramel": with_Caramel,
    "with_Flakes": with_Flakes,
    "with_Lid": with_Lid,
    "color": color
}

payload = json.dumps(data)

# Callback-Funktionen für MQTT-Verbindung
def on_connect(client, userdata, flags, rc):
    print("Verbunden mit dem MQTT-Broker. Rückgabewert: " + str(rc))

def on_disconnect(client, userdata, rc):
    print("Verbindung zum MQTT-Broker getrennt")

# Funktion zum Senden einer Nachricht über MQTT
def send_message(topic, message):
    client.publish(topic, message)
    print(f"Nachricht '{message}' wurde an das Topic '{topic}' gesendet.")

def on_publish(client, userdata, mid):
    print(f"Message {mid} published successfully.")

# Funktion zum Anzeigen des Menüs
def show_menu():
    print("\n--- TestShop ---")
    print("1. Vanille Joghurt")
    print("2. Erdbeer Joghurt")
    print("3. Blaubeer Joghurt")
    print("0. Beenden")

# Funktion zum Benutzerinput abfragen
def get_user_input(prompt):
    return input(prompt)

# Hauptfunktion
def main():
    # MQTT-Client initialisieren und Verbindung herstellen
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.connect(broker_address, port)
    client.loop_start()


    while True:
        show_menu()
        user_choice = get_user_input("Wähle eine Option: ")

        if user_choice == "1":
            # Konfiguration für Vanille Joghurt
            color = "WHITE"
            with_CaramelString = get_user_input("Mit Karamell: ")
            if with_CaramelString.lower() == "ja":
                with_Caramel = True
                print("mit Caramel")
            else:
                with_Caramel = False

            with_FlakesString = get_user_input("Mit Flakes: ")
            if with_FlakesString.lower() == "ja":
                with_Flakes = True
                print("mit Flakes")

            else:
                with_Flakes = False

            with_LidString = get_user_input("Mit recycelbarem Deckel: ")
            if with_LidString.lower() == "ja":
                with_Lid = True
                print("mit Deckel")
            else:
                with_Lid = False



        elif user_choice == "2":
            # Konfiguration für Erdbeer Joghurt
            color = "RED"
            with_CaramelString = get_user_input("Mit Karamell: ")
            if with_CaramelString.lower() == "ja":
                with_Caramel = True
            else:
                with_Caramel = False

            with_FlakesString = get_user_input("Mit Flakes: ")
            if with_FlakesString.lower() == "ja":
                with_Flakes = True
            else:
                with_Flakes = False

            with_LidString = get_user_input("Mit recycelbarem Deckel: ")
            if with_LidString.lower() == "ja":
                with_Lid = True
            else:
                with_Lid = False


        elif user_choice == "3":
            # Konfiguration für Blaubeer Joghurt
            color = "BLUE"
            with_CaramelString = get_user_input("Mit Karamell: ")
            if with_CaramelString.lower() == "ja":
                with_Caramel = True
            else:
                with_Caramel = False

            with_FlakesString = get_user_input("Mit Flakes: ")
            if with_FlakesString.lower() == "ja":
                with_Flakes = True
            else:
                with_Flakes = False

            with_LidString = get_user_input("Mit recycelbarem Deckel: ")
            if with_LidString.lower() == "ja":
                with_Lid = True
            else:
                with_Lid = False


        elif user_choice == "0":
            break

        else:
            print("Ungültige Eingabe. Bitte wähle eine Option aus dem Menü.")

        #neuer Payload für json
        data = {
            "name": name,
            "with_Caramel": with_Caramel,
            "with_Flakes": with_Flakes,
            "with_Lid": with_Lid,
            "color": color
        }
        payload = json.dumps(data)
        print(f"{payload}")
        client.publish(topic, payload)





    # Produktinformationen über MQTT senden
    #client.publish(topic, payload)

    # MQTT-Client beenden
    client.loop_stop()
    client.disconnect()
    print("Programm beendet.")

if __name__ == "__main__":
    main()
