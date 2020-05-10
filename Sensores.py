#%% Import Libraries
import paho.mqtt.client as mqtt
import time
import psutil
import json
from time import sleep
from w1thermsensor import W1ThermSensor
import logging
import mh_z19

#%% Read Temperature
def read_temp(sensor):
  if temp_sensor is not None :
    return sensor.get_temperature()
  else:
    logger.info("[{}] Not temp sensor : ".format('RP'))
    return None

#%% Read CO2
def read_co2():
  CO = mh_z19.read()
  if CO is not None :
    return CO['co2']
  else:
    logger.info("[{}] Not CO2 sensor : ".format('RP'))
    return None

#%% Define client
if __name__ == "__main__":
  client = mqtt.Client()
  client.connect('35.203.15.169', 1883, 60)
  client.loop_start()
  TOPIC = "sensors"

#%% Start Logger
  logging.basicConfig(level=logging.INFO, format='%(asctime)s  - [%(levelname)s] %(message)s')
  logger = logging.getLogger(__name__)

#%% Connect temperature sensor
  try :
    temp_sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "011453ea62aa")
  except:
    temp_sensor = None

  logger.info("[{}] Starting infinit loop".format('RP')) #Registros gringos but it's ok

#%% Send data
  while True:
    data = {"ts": int(1000*time.time()),
            "values":{"Temperature": read_temp(temp_sensor),
                      "CO2": read_co2(),
                      "RPmemory": round(psutil.virtual_memory().percent)
                      }
            }

    client.publish(TOPIC, json.dumps(data), 1)
    time.sleep(5)

