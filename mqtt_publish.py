'''Publish topics to mqtt broker'''

__author__ = "Lukas Beck"
__email__ = "st166506@stud.uni-stuttgart.de"
__copyright__ = "Lukas Beck"

__license__ = "GPL"
__version__ = "2024.03.09"

import json
import paho.mqtt.client as mqtt
import time

line_configs1 = [
    {
        "name": "Line1s", 
        "run": True,
        "start_at": "start",
        "end_at": "storage",
        "with_oven": True,
        "with_saw": True,
        "with_PM": True,
        "color": "WHITE",
    },
    {
        "name": "Line2w", 
        "run": True,
        "start_at": "storage",
        "end_at": "end",
        "color": "WHITE",
        "start_when": "Line1s",
    },
]

line_configs4 = [
    {
        "name": "Init", 
        "run": True,
        "start_at": "INIT",
        "end_at": "END"
    },
    {
        "name": "Line1", 
        "run": True,
        "start_at": "start",
        "end_at": "end",
        "with_oven": True,
        "with_saw": True,
        "color": "WHITE",
    },
    {
        "name": "Line2s", 
        "run": True,
        "start_at": "start",
        "end_at": "storage",
        "with_saw": True,
        "with_PM": True,
        "color": "RED",
    },
    {
        "name": "Line2w", 
        "run": True,
        "start_at": "storage",
        "end_at": "end",
        "color": "RED",
        "start_when": "Line2s",
    },
    {
        "name": "Line3", 
        "run": True,
        "start_at": "start",
        "end_at": "end",
        "color": "BLUE",
    },
    {
        "name": "Line4w", 
        "run": True,
        "start_at": "storage",
        "end_at": "END",
        "color": "RED",
        "end_int": True,
    },
    {
        "name": "Line4s", 
        "run": True,
        "start_at": "start",
        "end_at": "storage",
        "with_oven": True,
        "color": "RED",
        "start_int": True,
        "start_when": "Line4w",
    }
]

init_config = [
    {
        "name": "Init", 
        "run": True,
        "start_at": "INIT",
        "end_at": "END"
    },
]

line_configs_continues_start = [
    {
        "name": "Line1w", 
        "run": True,
        "start_at": "storage",
        "end_at": "END",
        "color": "WHITE",
    },
    {
        "name": "Line2w", 
        "run": True,
        "start_at": "storage",
        "end_at": "END",
        "color": "RED",
    },
    {
        "name": "Line3w", 
        "run": True,
        "start_at": "storage",
        "end_at": "END",
        "color": "BLUE",
    },
]

line_configs_continues = [
    {
        "name": "Line1s", 
        "run": True,
        "start_at": "start",
        "end_at": "storage",
        "with_oven": True,
        "with_saw": True,
        "color": "WHITE",
        "restart": True,
        "start_when": "Line1w",
        "start_int": True,
    },
    {
        "name": "Line1w", 
        "run": True,
        "start_at": "storage",
        "end_at": "END",
        "color": "WHITE",
        "restart": True,
        "start_when": "Line1s",
        "end_int": True,
    },
    {
        "name": "Line2s", 
        "run": True,
        "start_at": "start",
        "end_at": "storage",
        "with_PM": True,
        "color": "RED",
        "restart": True,
        "start_when": "Line2w",
        "start_int": True,
    },
    {
        "name": "Line2w", 
        "run": True,
        "start_at": "storage",
        "end_at": "END",
        "color": "RED",
        "restart": True,
        "start_when": "Line2s",
        "end_int": True,
    },
    {
        "name": "Line3s", 
        "run": True,
        "start_at": "start",
        "end_at": "storage",
        "color": "BLUE",
        "restart": True,
        "start_when": "Line3w",
        "start_int": True,
    },
    {
        "name": "Line3w", 
        "run": True,
        "start_at": "storage",
        "end_at": "END",
        "with_mill": True,
        "with_drill": True,
        "color": "BLUE",
        "restart": True,
        "start_when": "Line3s",
        "end_int": True,
    },
]

factory_config = {
    "exit_if_end": True
}

factory_command = {
    "run": True,
    "stop": False
}

wh_content = [
    [
        "WHITE",
        "RED",
        "BLUE"
    ],
    [
        "Carrier",
        "Carrier",
        "Empty"
    ],
    [
        "Empty",
        "Empty",
        "Empty"
    ]
]

class MqttPublish():
    '''Handels Publishing to mqtt broker.
    '''

    __BROKER_ADDR = "MiniFactory"
    __PORT = 1883

    def __init__(self, std_factory: str, std_config) -> None:
        '''Init MqttInterface.'''

        # self.__BROKER_ADDR = "test.mosquitto.org"

        self.line_config = std_config
        self.factory_side = std_factory
        self.set_topics()

        self.client = mqtt.Client()

        self.client.connect(self.__BROKER_ADDR, self.__PORT)


    def set_topics(self):
        self.topic_start = f"MiniFactory/{self.factory_side}/Factory"

        self.topic_line_config_set = f"{self.topic_start}/LineConfig/Set"
        self.topic_factory_config_set = f"{self.topic_start}/FactoryConfig/Set"
        self.topic_factory_command_set = f"{self.topic_start}/FactoryCommand/Set"
        self.topic_wh_content_set = f"{self.topic_start}/WHContent/Set"

        self.topic_line_config_get = f"{self.topic_start}/LineConfig/Get"
        self.topic_factory_config_get = f"{self.topic_start}/FactoryConfig/Get"
        self.topic_factory_command_get = f"{self.topic_start}/FactoryCommand/Get"
        self.topic_wh_content_get = f"{self.topic_start}/WHContent/Get"
        self.topic_machine_status_get = f"{self.topic_start}/MachineStatus/Get"
        self.topic_line_status_get = f"{self.topic_start}/LineStatus/Get"


    def publish_get(self) -> bool:
        while True:
            print("Publish program for the MiniFactory, enter the character for the corresponding option:")
            print("c: get Line config")
            print("l: get Line status")
            print("w: get Warehouse content")
            print("m: get Machine status")
            print("f: get Factory commands")
            print("s: show setter functions")
            print("e: exit the publish program")
            char = input("Enter the character: ").lower()[0]
            self.client.connect(self.__BROKER_ADDR, self.__PORT)
            if char == "c":
                self.client.publish(self.topic_line_config_get)
            elif char == "l":
                self.client.publish(self.topic_line_status_get)
            elif char == "w":
                self.client.publish(self.topic_wh_content_get)
            elif char == "m":
                self.client.publish(self.topic_machine_status_get)
            elif char == "f":
                self.client.publish(self.topic_factory_command_get)
            elif char == "s":
                return False
            elif char == "e":
                return True

    def publish_set(self):
        while True:
            print("\nPublish program for the MiniFactory, enter the character for the corresponding option:")
            print("s: start factory (sends line_configs, wh_configs and start command)")
            print("r: restart factory after PROBLEM occurred (sends a start command)")
            print("x: stops the factory")
            print("p: pauses the factory")
            print("c: change config to be send")
            print("f: change Factory side")
            print("g: show getter functions")
            print("e: exit the publish program")
            char = input("Enter the character: ").lower()[0]
            self.client.connect(self.__BROKER_ADDR, self.__PORT)
            if char == "s":
                self.client.publish(self.topic_wh_content_set, json.dumps(wh_content))
                for config in self.line_config:
                    self.client.publish(self.topic_line_config_set, json.dumps(config))
                time.sleep(0.5)
                self.client.publish(self.topic_factory_command_set, json.dumps({"run": True}))
                if self.line_config == line_configs_continues_start:
                    time.sleep(1)
                    for config in line_configs_continues:
                        self.client.publish(self.topic_line_config_set, json.dumps(config))
            elif char == "r":
                self.client.publish(self.topic_factory_command_set, json.dumps({"run": True}))
            elif char =="x":
                self.client.publish(self.topic_factory_command_set, json.dumps({"stop": True}))
            elif char == "p":
                self.client.publish(self.topic_factory_command_set, json.dumps({"run": False}))
            elif char == "g":
                if self.publish_get():
                    return
            elif char == "c":
                print(f"\nChanging config to be send:")
                print(f"i: set factory to initial state.")
                print(f"1: one line from Start to end.")
                print(f"2: four lines with different paths")
                print(f"3: Runs a loop indefinitely")
                char = input("Enter the character: ").lower()[0]
                if char == "i":
                    self.line_config = init_config
                    print("Changed to init config")
                elif char == "1":
                    self.line_config = line_configs1
                    print("Changed to line configs 1")
                elif char == "2":
                    self.line_config = line_configs4
                    print("Changed to line configs 4")
                elif char == "3":
                    self.line_config = line_configs_continues_start
                    print("Changed to line configs continues")
                else:
                    print(f"'{char}' not recognized please try again")
            elif char == "f":
                print(f"\nChanging factory side, current side is: {self.factory_side}")
                print("r: change to Right side")
                print("l: change to Left side")
                char = input("Enter the character: ").lower()[0]
                if char == "r":
                    self.factory_side = "Right"
                elif char == "l":
                    self.factory_side = "Left"
                else:
                    print(f"{char}: no available.")
                    continue
                print(f"Changed side to {self.factory_side}")
                self.set_topics()
            elif char == "e":
                return
            else:
                print(f"'{char}' not recognized please try again")

if __name__ == "__main__":
    mqtt_pub = MqttPublish(std_factory="Right", std_config=line_configs_continues_start)

    mqtt_pub.publish_set()
    

    print("end")