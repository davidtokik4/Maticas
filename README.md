# Proyecto Maticas

Proyecto dividido por devices

## Modulos
Los process correspondienestes a cada módulo son:
1. Control: tb_mqtt2.py
2. Sensores
3. Actuadores X3
4. Actuadores X9

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