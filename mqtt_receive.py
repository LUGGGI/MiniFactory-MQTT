'''Handels Communication with mqtt broker.

Topics: MiniFactory/Right/Factory/LineConfig
'''

__author__ = "Lukas Beck"
__email__ = "st166506@stud.uni-stuttgart.de"
__copyright__ = "Lukas Beck"

__license__ = "GPL"
__version__ = "2024.02.28"

import json
import paho.mqtt.client as mqtt
from logger import log

# set the wanted factory
# FACTORY = "Right"
# FACTORY = "Left"
FACTORY = "+" # can receive both

class MqttReceive():
    '''Handels Receiving with mqtt broker.
    '''

    __BROKER_ADDR = "MiniFactory"
    __PORT = 1883
    

    def __init__(self, factory_name: str) -> None:
        '''Init MqttInterface.
        
        Args:
            factory_name (str): Name of the factory (for example Right).
            states (State): Possible States of line.
        '''

        # self.__BROKER_ADDR = "test.mosquitto.org"

        self.topic_start = f"MiniFactory/{factory_name}/Factory"

        self.log = log
        self.message_count = 0

        
        self.client = mqtt.Client()
        self.client.on_connect = self.__on_connect

        self.client.on_message = self.__on_message_fallback

        self.client.on_disconnect = self.__on_disconnect

        self.client.connect(self.__BROKER_ADDR, self.__PORT)

        self.client.loop_forever()



    def disconnect(self):
        '''Disconnect from MQTT broker.'''
        self.client.disconnect()


    def __on_connect(self, client: mqtt.Client, _userdata, _flags, rc):
        '''Connection callback.
        
        Args:
            client(mqtt.Client): connection client.
        '''
        self.log.debug(f"Connected to MQTT-Broker. Result code: {rc}")

        client.subscribe("#")
        # client.subscribe(f"{self.topic_start}/#")
        # client.subscribe(f"{self.__topic_start}/+/Get")
        # client.subscribe(f"{self.__topic_start}/+/Set")
        # client.subscribe(f"{self.__topic_start}/+/Data")
        # client.subscribe("Debug")
        # client.subscribe("Status")

    def __on_message_fallback(self, _client, _userdata, msg: mqtt.MQTTMessage):
        '''Callback for new message that couldn't be filtered in other callbacks.'''
        try:
            decoded_msg = json.loads(msg.payload)
        except Exception:
            decoded_msg = msg.payload

        self.message_count += 1
        self.log.info(f"{self.message_count}; {msg.topic.removeprefix(f'{self.topic_start}/')}; {decoded_msg}")


    def __on_disconnect(self, client, userdata, rc):
        '''Disconnection callback.'''
        print("Connection to MQTT-Broker disconnected")    


if __name__ == "__main__":
    MqttReceive(factory_name=FACTORY)