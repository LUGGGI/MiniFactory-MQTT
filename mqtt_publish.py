'''Publish topics to mqtt broker
'''

__author__ = "Lukas Beck"
__email__ = "st166506@stud.uni-stuttgart.de"
__copyright__ = "Lukas Beck"

__license__ = "GPL"
__version__ = "2024.01.19"

import json
import paho.mqtt.client as mqtt
import time


read = True

line_configs1 = [
    {
        "name": "Line1", 
        "run": True,
        "start_at": "start",
        "end_at": "END",
        "with_oven": True,
        "with_saw": True,
        "with_PM": True,
        "with_WH": True,
        "color": "WHITE"
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
        "end_at": "END",
        "with_oven": True,
        "with_saw": True,
        "with_PM": False,
        "with_WH": False,
        "color": "WHITE"
    },
    {
        "name": "Line2", 
        "run": True,
        "start_at": "start",
        "end_at": "storage",
        "with_oven": False,
        "with_saw": True,
        "with_PM": True,
        "with_WH": True,
        "color": "RED"
    },
    {
        "name": "Line3", 
        "run": True,
        "start_at": "start",
        "end_at": "END",
        "with_PM": False,
        "color": "BLUE"
    },
    {
        "name": "Line4", 
        "run": True,
        "start_at": "storage",
        "end_at": "END",
        "color": "RED"
    }
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
            "Carrier",
            "Carrier",
            "Carrier"
        ],
        [
            "WHITE",
            "RED",
            "BLUE"
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

    __BROKER_ADDR = "192.168.0.59"
    __PORT = 1883

    def __init__(self) -> None:
        '''Init MqttInterface.'''

        self.__BROKER_ADDR = "test.mosquitto.org"

        self.line_config = line_configs4
        self.factory_side = "Right"
        self.topic_start = f"MiniFactory/{self.factory_side}/Factory"

        self.client = mqtt.Client()

        self.client.connect(self.__BROKER_ADDR, self.__PORT)


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


    def publish_all(self):
        
        
        self.client.publish(self.topic_wh_content_set, json.dumps(wh_content))
        print(f"{self.topic_wh_content_set.removeprefix(f'{self.topic_start}/')}")

        # self.client.publish(self.topic_line_config_set, json.dumps({
        #     "name": "Test",
        #     "run": True,
        #     "start_at": "storage",
        #     "end_at": "CB5",
        #     "color": "RED"
        # }))
        # self.client.publish(self.topic_line_config_set, json.dumps({
        #     "name": "Line1", 
        #     "run": True,
        #     "start_at": "start",
        #     "end_at": "END",
        #     "with_oven": False,
        #     "with_saw": True,
        #     "with_PM": True,
        #     "with_WH": True,
        #     "color": "WHITE"
        # }))


        # return

        # self.client.publish(self.topic_factory_command_set, json.dumps({"stop": True}))
        # print(f"{self.topic_factory_command_set.removeprefix(f'{self.topic_start}/')}")
        
        for config in line_configs:
            self.client.publish(self.topic_line_config_set, json.dumps(config))
            print(f"{self.topic_line_config_set.removeprefix(f'{self.topic_start}/')}")

        time.sleep(0.5)

        self.client.publish(self.topic_factory_command_set, json.dumps({"run": True}))
        print(f"{self.topic_factory_command_set.removeprefix(f'{self.topic_start}/')}")

        # self.client.publish(self.topic_line_config_get)
        # print(f"{self.topic_line_config_get.removeprefix(f'{self.topic_start}/')}")

        # self.client.publish(self.topic_line_status_get)
        # print(f"{self.topic_line_status_get.removeprefix(f'{self.topic_start}/')}")

        # time.sleep(1)
            
        # self.client.publish(self.topic_factory_command_set, json.dumps({"run": True}))
        # print(f"{self.topic_factory_command_set.removeprefix(f'{self.topic_start}/')}")

        # time.sleep(1)

        # self.client.publish(self.topic_line_config_get)
        # print(f"{self.topic_line_config_get.removeprefix(f'{self.topic_start}/')}")

        # self.client.publish(self.topic_line_status_get)
        # print(f"{self.topic_line_status_get.removeprefix(f'{self.topic_start}/')}")

        # time.sleep(1)


        # self.client.publish(self.topic_factory_config_set, json.dumps({"exit_if_end": True}))
        # print(f"{self.topic_factory_config_set.removeprefix(f'{self.topic_start}/')}")

        # time.sleep(3)

        # self.client.publish(self.topic_wh_content_get)
        # print(f"{self.topic_wh_content_get.removeprefix(f'{self.__topic_start}/')}")

        # # todo get working 
        # self.client.publish(self.topic_line_config_get)
        # print(f"{self.topic_line_config_get.removeprefix(f'{self.__topic_start}/')}")

        # self.client.publish(self.topic_factory_config_get)
        # print(f"{self.topic_factory_config_get.removeprefix(f'{self.__topic_start}/')}")

        print("End of publish all")


    def publish_get(self) -> bool:
        while True:
            print("Publish program for the MiniFactory, enter the character for the corresponding option:")
            print("c: get Line config")
            print("l: get Line status")
            print("w: get Warehouse content")
            print("m: get Machine status")
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
            print("g: show getter functions")
            print("c: change config to be send")
            print("f: change Factory side")
            print("e: exit the publish program")
            char = input("Enter the character: ").lower()[0]
            self.client.connect(self.__BROKER_ADDR, self.__PORT)
            if char == "s":
                self.client.publish(self.topic_wh_content_set, json.dumps(wh_content))
                for config in self.line_config:
                    self.client.publish(self.topic_line_config_set, json.dumps(config))
                time.sleep(0.5)
                self.client.publish(self.topic_factory_command_set, json.dumps({"run": True}))
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
                print(f"1: one line from Start to end.")
                print(f"4: four lines with different paths")
                char = input("Enter the character: ").lower()[0]
                if char == "1":
                    self.line_config = line_configs1
                    print("Changed to line configs 1")
                elif char == "4":
                    self.line_config = line_configs4
                    print("Changed to line configs 4")
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
                self.topic_start = f"MiniFactory/{self.factory_side}/Factory"
            elif char == "e":
                return
            else:
                print(f"'{char}' not recognized please try again")

if __name__ == "__main__":
    mqtt_pub = MqttPublish()

    mqtt_pub.publish_set()
    

    print("end")