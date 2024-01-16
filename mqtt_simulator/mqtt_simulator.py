'''Uses a prerecored mqtt message file to replay all the mqtt messages
'''

__author__ = "Lukas Beck"
__email__ = "st166506@stud.uni-stuttgart.de"
__copyright__ = "Lukas Beck"

__license__ = "GPL"
__version__ = "2024.01.16"

import csv
import paho.mqtt.client as mqtt
import logging
from datetime import datetime
from time import sleep
import time





class MqttHandler():
    '''Handels Publishing to mqtt broker.
    '''

    __BROKER_ADDR = "192.168.0.59"
    __PORT = 1883

    def __init__(self, topic_start: str) -> None:
        '''Init MqttInterface.
        
        Args:
            factory_name (str): Name of the factory (for example Right).
            states (State): Possible States of line.
        '''

        self.__BROKER_ADDR = "test.mosquitto.org"

        self.topic_start = topic_start

        self.client = mqtt.Client()

        self.client.connect(self.__BROKER_ADDR, self.__PORT)


    def publish_msg(self, topic: str, msg: str):
        
        self.client.publish(f"{self.topic_start}/{topic}")


class Logger():
    STD_LEVEL_CONSOLE = "WARNING"
    LEVEL_FILE = logging.INFO


    def __init__(self) -> None:
            
        self.log: logging.Logger = None


        # log_file_path = f"log_mqtt/mqtt{listdir('log_mqtt').__len__()+1}.log"


        log_formatter_file = logging.Formatter("%(asctime)s.%(msecs)03d; %(message)s", datefmt='%H:%M:%S')
        log_formatter_console = logging.Formatter("%(asctime)s.%(msecs)03d; %(message)s", datefmt='%M:%S')

        # Setup File handler, change mode tp 'a' to keep the log after relaunch
        # file_handler = logging.FileHandler(log_file_path, mode='a')
        # file_handler.setFormatter(log_formatter_file)
        # file_handler.setLevel(self.LEVEL_FILE)

        # Setup Stream Handler (i.e. console)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(log_formatter_console)
        stream_handler.setLevel(logging.DEBUG)

        # Get our logger
        self.log = logging.getLogger()
        self.log.setLevel(logging.DEBUG)

        # Add both Handlers
        self.log.addHandler(stream_handler)
        # self.log.addHandler(file_handler)


class LogReader():
    def __init__(self, file: str, mqtt_handler: MqttHandler, log: logging.Logger) -> None:
        self.mqtt_handler = mqtt_handler

        log_file = open(file)

        start_time = datetime.now()
        preveus_msg_time: datetime = None
        log_start_time:datetime = None

        log_reader = csv.reader(log_file, delimiter=';', skipinitialspace=True)


        for row in log_reader:
            row[0] = datetime.strptime(row[0], "%H:%M:%S.%f")
            row[1] = int(row[1])
            if log_reader.line_num == 1:
                log_start_time = row[0]
                log.warning(f"Log start time at: {log_start_time}; {row[2]}")

            else:
                
                while (True):
                    if (datetime.now() - start_time) > (row[0] - log_start_time):
                        log.info(row)
                        break
                    else:
                        print(f"{((datetime.now() - start_time) - (row[0] - log_start_time)).microseconds/1000000} : {(datetime.now() - start_time).microseconds/1000000}:  {(row[0] - log_start_time).microseconds/1000000}")
                        sleep(((datetime.now() - start_time) - (row[0] - log_start_time)).microseconds/1000000)

            


if __name__ == "__main__":
    logger = Logger()
    mqtt_handler = MqttHandler("MiniFactory/Right/Factory")
    LogReader("mqtt_simulator/mqtt4.log", mqtt_handler, logger.log)