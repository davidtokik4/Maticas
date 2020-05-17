# Proyecto Maticas

Proyecto dividido por devices

## Modulos
Los process correspondienestes a cada módulo son:
1. Control: tb_mqtt2.py
2. Sensores
3. Actuadores X3
4. Actuadores X9

## Configuración de Red
La siguiente imagen presenta los componentes principales de la red
![Image of network](/network.jpg)

SSID = maticas_net \
pass = yatusabe

1. Servidor MQTT (Thingsboard) 192.168.0.1
2. Base de datos (Influx con Chronograph) 192.168.0.1
3. Controladores (RP3) 192.168.0.NX
4. Sensores (RP ZERO) 192.168.0.NX

## Librerias
Las siguientes lbrerias son usadas en python 3.7
```python
    import paho.mqtt
    import time
    import psutil
    import argparse
    import json
    import gpiozero
    import w1thermsensor
    import datetime
    import logging
    import mh_z19
    import aioschedule
    import asyncio
```

## Licencia
[Copyright](https://github.com/davidtokik4/Maticas/blob/master/LICENSE.md)