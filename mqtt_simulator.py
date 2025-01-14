'''Uses a prerecorded mqtt message file to replay all the mqtt messages

Howto:
 - call from MQTT directory 
 - Only change values at bottom
 - Set file in LogReader to wanted recording
 - Set scaler in LogReader to play slower or faster(lower values sends the messages faster)
 - In MqttHandler set right broker and topic_start
 - Call with py .\mqtt_simulator.py under windows or equivalent in other systems
'''

__author__ = "Lukas Beck"
__email__ = "st166506@stud.uni-stuttgart.de"
__copyright__ = "Lukas Beck"

__license__ = "GPL"
__version__ = "2024.01.19"

import csv
import paho.mqtt.client as mqtt
import logging
from datetime import datetime
from time import sleep

import ast
import json

class MqttHandler():
    '''Handels Publishing to mqtt broker.
    '''

    
    __PORT = 1883

    def __init__(self, broker_addr: str, topic_start: str) -> None:
        '''Init MqttInterface.
        
        Args:
            topic_start(str): string to parse to the beginning of the topic
        '''
        self.topic_start = topic_start

        self.client = mqtt.Client()

        self.client.connect(broker_addr, self.__PORT)


    def publish_msg(self, topic: str, msg: str):
        try:
            msg = json.dumps(ast.literal_eval(msg))
        except Exception:
            msg = json.dumps({"msg": msg}) # uncomment to convert strings to dictionaries
            pass
        self.client.publish(f"{self.topic_start}{topic}", msg)


class Logger():
    '''Handles logging'''
    STD_LEVEL_CONSOLE = "WARNING"
    LEVEL_FILE = logging.INFO


    def __init__(self) -> None:
            
        self.log: logging.Logger = None

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
    '''Handles the reading an timing of the messages'''
    def __init__(self, file: str, mqtt_handler: MqttHandler, log: logging.Logger, scaler=1.0) -> None:
        '''Init LogReader.
        
        Args:
            file(str): the log file to read
            mqtt_handler: object to the mqtt_handler
            log: object to Logger
            scaler: value the scale the sending time, lover values send faster
        '''
        log_file = open(file)

        start_time = datetime.now()
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
                    log_time_dif = (row[0] - log_start_time) * scaler
                    current_time_dif = datetime.now() - start_time
                    if current_time_dif > log_time_dif:
                        mqtt_handler.publish_msg(row[2], row[3])
                        log.info(row)
                        break
                    else:
                        # print(f"{(log_time_dif - current_time_dif).total_seconds()} : {current_time_dif.total_seconds()}:  {log_time_dif.total_seconds()}")
                        sleep((log_time_dif - current_time_dif).total_seconds())

if __name__ == "__main__":

    # BROKER_ADDR = "MiniFactory" #direct connection to the MiniFactory broker
    BROKER_ADDR = "test.mosquitto.org" # test broker works everywhere
    TOPIC_START = ""
    # TOPIC_START = "MiniFactory/Right/Factory/"


    logger = Logger()
    mqtt_handler = MqttHandler(BROKER_ADDR, topic_start=TOPIC_START)
    LogReader(file="mqtt_log_save/line1.log", mqtt_handler=mqtt_handler, log=logger.log, scaler=1.0)