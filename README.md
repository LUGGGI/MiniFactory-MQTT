# Anleitung für MQTT mit der Fabrik

Anleitung für Fabrik laufen lassen nach derzeitigem Stand:

* den [lugggi_implement_mqtt_simulator](https://github.tik.uni-stuttgart.de/IAS-MiniFactory/MQTT/tree/lugggi_implement_mqtt_simulator) brach im MQTT repository clonen und checkout machen.
* Strom für die Fabrik anmachen
* die mqtt_publish.py datei mit python ausführen.
* die gewünschte option da auswählen, alle Optionen werden im Programm Menu aufgeführt, die wichtigsten sind:
  * s: Vier Produkte wie gewohnt über die Fabrik laufen lassen (nachlegen am Eingang nicht vergessen)
  * r: wenn die Fabrik wegen einem problem stoppt kann man das hiermit wieder starten.
  * f: Fabrik Seite ändern. Standard ist die rechte Seite.
* Falls  man die mqtt Sendungen der Fabrik sehen möchte, die mqtt_receive.py Datei parallel laufen lassen. (Achtung hier muss ganz oben die gewünschte Seite ausgewählt werden, std ist die Rechte Seite)
* man kann dann auch mit den getter Funktionen in mqtt_publish sich status der fabrik, produktionlinien oder maschinen anzeigen lassen.

# Anleitung Simulator

* Terminal in dem Ordner MQTT öffnen.
  * Dateipfand zum Ausführung muss .../MQTT/ sein nicht im Ordner mqtt_simulator.
* Werte ganz unten in der Datei anpassen.
  * file in LogReader zu der gewünschten Aufzeichnung stellen
  * scaler in LogReader kann verändert werden um das Aufgezeichnete schneller (value < 1) oder langsamer (value > 1) abspielen zu lassen
  * in MqttHandler Broker und topic_start einstellen
* `python .\mqtt_simulator\mqtt_simulator.py` ausführen (unter windows kann auch `py .\mqtt_sim...` sein)
