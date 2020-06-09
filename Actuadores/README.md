# Módulo de Actuadores
Este módulo tiene las siguientes rutinas de luces, vuelticas y riego
1. Los primeros 8min de cada hora se enciende la bomba
2. Las luces se encienden a las 7am y se apagan a las 7pm
3. El riego y el giro se encienden al tiempo always

## Setup Raspberry Zero
Para empezar la RP desde zero:
1. Instalar Raspbian Lite con imager en la microSD
2. Poner la SD en la raspberry (Kernel para Zero, kernel7 para 3 y 3B+, kernel7l para 4) y conectar pantalla y teclado
3. Login
```Bash
login: pi
pass: raspberry
```
4. Agregar red wifi
```Bash
$ sudo -s
$ cd .. # until home
$ nano /etc/wpa_supplicant/wpa_supplicant.conf
```

5. Agregar la red al final
```Bash
country=CA
network={
    ssid="maticas_net"
    psk="yatusabe"
}
```
6. Probar con ifconfig o ping que está conectado a la red
7. Activar el SSH
```Bash
$ raspi-config
Interfacing options > Enable SSH
Network options > HostName > SensorX
```
8. Conectar por SSH
9. Copiar actuadores.py al directorio home/pi
10. Remover python 2.7
```Bash
$ sudo apt-get remove python2.7
$ sudo apt-get autoremove
```
11. Instalar python 3.7.8
```Bash
$ sudo apt-get update
$ sudo apt-get install -y build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev tar wget vim
$ wget https://www.python.org/ftp/python/3.8.3/Python-3.8.3.tgz
$ sudo tar zxf Python-3.8.3.tgz
$ cd Python-3.8.3
$ sudo ./configure --enable-optimizations
$ sudo make -j 4 #Este comando se demora en la RP zero
$ sudo make altinstall
$ echo "alias python=/usr/local/bin/python3.8" >> ~/.bashrc
$ source ~/.bashrc
```
12. Instalar pip
```Bash
$ sudo apt-get install python3-pip
```
13. Instalar librerías
```Bash
$ pip3 install paho-mqtt
$ pip3 install psutil
$ pip3 install json
$ pip3 install logging
$ pip3 install asyncio
$ pip3 install aioschedule
```
14. Set la zona horaria desde raspi-config

## Conexión de Salidas
Son tres pines de salida:
1. Luces GPIO 0 y 1
2. Giro GPIO 2
3. Bomba GPIO 3

![pinout](https://www.raspberrypi.org/documentation/usage/gpio/images/GPIO-Pinout-Diagram-2.png)

## Iniciar el script
El script comienza atomáticamente con supervisord
1. Cambiar el AccesToken en actuadores.py por el que da la dashboard para cada raspberry
2. Instalar supervisord
```Bash
$ sudo apt-get install supervisor
```
3. Configurar supervisord con el script
```Bash
$ cd /etc/supervisor/conf.d/
$ sudo nano actuadores.conf
```
4. Agregar la configuración 
```Python
[program:actuadores]
directory = /home/pi/
command = sudo python3 actuadores.py
user = root
password = raspberry
autosart = true
identifier = sensores
autorestart = true
startretries = 20
stdout_logfile=/var/log/supervisor/sensores.log
```

## Revisar 
En el servidor de Thingsboard se debe configurar los widgets que envíen señales de activación a los GPIO

Revisar también que los relés se activen

Revisar los logs en
```Bash
$ cd /var/log/supervisor/Program.log
```