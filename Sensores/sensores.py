#%% Import Libraries
import paho.mqtt.client as mqtt
import time
import psutil
import json
from time import sleep
from w1thermsensor import W1ThermSensor
import logging
import mh_z19
import Adafruit_DHT

#%% Read Temperature
def read_temp():
    # if temp_sensor is not None :
    #   return sensor.get_temperature()
    # else:
    #   logger.info("[{}] Not temp sensor : ".format('RP'))
    #   return None
    humidity1, temperature1 = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4)
    # humidity2, temperature2 = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 3)
    # humidity3, temperature3 = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4)
    # humidity4, temperature4 = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 5)
    # return [temperature1, temperature2, temperature3, temperature4], [humidity1, humidity2, humidity3, humidity4]
    return temperature1, humidity1


#%% Read CO2
def read_co2():
    CO = mh_z19.read_all()
    if CO is not None and isinstance(CO,dict):
        return CO["co2"], CO["temperature"]
    else:
        logger.info("[{}] Not CO2 sensor : ".format("RP"))
        return None, None


#%% Define on connect
def on_connect(client, userdata, rc, *extra_params):
    print("Connected with result code " + str(rc))
    client.subscribe("v1/devices/me/rpc/request/+")
    # client.publish('v1/devices/me/attributes', get_gpio_status(), 1)


#%% Define client
if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.username_pw_set("MaSXZ5bWwgwEE2eaLCua")
    client.connect("155.138.133.71", port=1883, keepalive=60)
    client.loop_start()

    #%% Start Logger
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s  - [%(levelname)s] %(message)s"
    )
    logger = logging.getLogger(__name__)

    #%% Connect temperature sensor
    # try :
    #   temp_sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "011453ea62aa")
    # except:
    #   temp_sensor = None
    logger.info(
        "[{}] Starting infinit loop".format("RP")
    )  # Registros gringos but it's ok

    mh_z19.zero_point_calibration()
    mh_z19.detection_range_5000()
    mh_z19.detection_range_5000()

#%% Send data
    while True:
        temp1, humidity = read_temp()
        co2, temp2 = read_co2()
        data = {
            "ts": int(1000 * time.time()),
            "values": {
                "Temperature": temp2,
                "Humidity": humidity,
                "CO2": co2,
                "RPmemory": round(psutil.virtual_memory().percent),
            },
        }

        client.publish("v1/devices/me/telemetry", json.dumps(data), 1)
        time.sleep(5)

