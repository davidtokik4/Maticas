import paho.mqtt.client as mqtt
import time, psutil
import argparse
import json
from gpiozero import LEDBoard
from time import sleep
import datetime
import logging
import aioschedule as schedule
import asyncio

board = LEDBoard(21, 20, 16, 26, 19, 13, 6, 5, initial_value=False,active_high=False)
ligths_port = [0,1]
motors_port = 2
pumps_port = 3

#States = {'ligths':False,'pumps':False,'motors':False}
time.sleep(10)

logging.basicConfig(level=logging.INFO, format='%(asctime)s  - [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

mqtt_host = '155.138.133.71'
ACCESS_TOKEN = 'kIj8grkE1XTMirfxSEdJ'

confitopic = 'v1/devices/me/attributes'
teletopic = 'v1/devices/me/telemetry'
attributes = {"attribute":"Toki_test"}

#gpio_state = False

#def get_gpio_status(port):
#    logger.info("[{}] Get status of port {} : {}".format('THINGSBOARD', port, bool(board[port].value) ))
#    return json.dumps(bool(board[port].value))

#def set_gpio_status(port,status):
#    if status:
#      board[port].on()
#    else:
#      board[port].off()


def on_connect(client, userdata, flags, rc):
  client.publish(confitopic,json.dumps(attributes),1)
  logger.info("[{}] Connecting to broker {} with result code {}".format('THINGSBOARD',mqtt_host, str(rc)))
  client.subscribe('v1/devices/me/rpc/request/+')

def on_message(client, userdata, msg):
  data = json.loads(msg.payload.decode('utf8'))
  logger.info("[{}] Feedback message from : {}".format('THINGSBOARD',data))
  method = data['method']
  if method=='checkpump':
  client.publish(msg.topic.replace('request', 'response'), get_gpio_status(port=pumps_port), 1)

  wlist = method.split('_')
  if len(wlist)==2:
  port = int(wlist[1])
    if wlist[0] == 'getValue':
      client.publish(msg.topic.replace('request', 'response'), get_gpio_status(port), 1)
    elif wlist[0] == 'setValue':
      set_gpio_status(port,data['params'])
    client.publish(msg.topic.replace('request', 'response'), get_gpio_status(port), 1)
    client.publish('v1/devices/me/attributes', get_gpio_status(), 1)


##Pump and ligths coroutines
async def pumpjob(delay=8,port=pumps_port):
    board[port].on()
    if bool(board[motors_port].value) is False:
      board[motors_port].on()
      logger.info("[{}] Turning motors on".format('RP')) 
      
    logger.info("[{}] Turning pump on".format('RP'))          
    await asyncio.sleep(delay*60)
    logger.info("[{}] Turning pump off".format('RP'))
    board[port].off()
    if bool(board[ligths_port[0]].value) is False:
      board[motors_port].off()

async def ligthsjob(port=ligths_port,status=False):
    if status:
      logger.info("[{}] Turning ligths on".format('RP'))
      board[port[0]].on()
      board[port[1]].on()
      board[motors_port].on()
    else:
      logger.info("[{}] Turning ligths off".format('RP'))
      #board[port].off()
      board[port[0]].off()
      board[port[1]].off()
      if bool(board[pumps_port].value) is False:
        board[motors_port].off()
        
##Check time for ligths (when programm starts)
now_time = datetime.datetime.today().time()
if datetime.time(7, 0, 0) <= now_time or datetime.time(19, 0,0) >= now_time:
  logger.info("[{}] Turning ligths on".format('RP'))CO['co2']
  board[ligths_port[0]].on()
  board[ligths_port[1]].on()
  board[motors_port].on()
  
##Mqtt client settings
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(ACCESS_TOKEN)
client.connect(mqtt_host, 1883, 60)
client.loop_start()
time.sleep(1)


schedule.every().hour.do(job)
schedule.every().hour.at(':00').do(pumpjob, delay=6,port=pumps_port)
schedule.every().day.at("07:00").do(ligthsjob, port=ligths_port, status=True)
schedule.every().day.at("19:00").do(ligthsjob, port=ligths_port, status=False)
loop = asyncio.get_event_loop()

logger.info("[{}] Starting infinit loop".format('RP'))

while True:
  loop.run_until_complete(schedule.run_pending())
  mem = psutil.virtual_memory()
  data = {"ts":int(1000*time.time()),
          "values":{"RPmemory":round(mem.percent)}
          }
  client.publish(teletopic,json.dumps(data),1)
  # logger.info("[{}] Sending : {}".format('RP',data))
  time.sleep(15)

client.disconnect()
