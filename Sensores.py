import paho.mqtt.client as mqtt
import time, psutil
import argparse
import json
#from gpiozero import LEDBoard
from time import sleep
from w1thermsensor import W1ThermSensor
import datetime
import logging
import mh_z19
import aioschedule as schedule
import asyncio


teletopic = 'v1/devices/me/telemetry'
try :
  sensor = W1ThermSensor(W1ThermSensor.THERM_SENSOR_DS18B20, "011453ea62aa")
except:
  sensor = None

logger.info("[{}] Starting infinit loop".format('RP'))
#ADC = adc()


while True:

 # loop.run_until_complete(schedule.run_pending())

  if sensor is not None :
    T1 = sensor.get_temperature()
  else:
    T1 = None
    logger.info("[{}] Not temp sensor : ".format('RP'))
  #temps=psutil.sensors_temperatures()

  CO = mh_z19.read()
  if CO is not None :
    co2 = CO['co2']
  else:
    co2 = None
    logger.info("[{}] Not CO2 sensor : ".format('RP'))

  #Isensor = ADC.getreading(0)
  mem = psutil.virtual_memory()
  data = {"ts":int(1000*time.time()),
          "values":{"Temperature":T1,
                    #"Power":mem.percent,
                    #"Current":40.*Isensor,
                    "CO2":co2,
                    "RPmemory":round(mem.percent)
                    #"pump":board[ligths_port[0]].value
                    }
          }
  time.sleep()
