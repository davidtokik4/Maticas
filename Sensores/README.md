# Módulo de Sensores
Este módulo contiene 4 sensores de temperatura y un sensor de CO2

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
Another alternative without connecting HDMI is to create a file wpa_supplicant.conf into the SD and the RP will copy to the correct location at first run
```Bash
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=CA

network={
 ssid="maticas_net"
 psk="yatusabe"
}
```
And then put an empty file called ssh without extension in the SD card

6. Probar con ifconfig o ping que está conectado a la red
7. Activar el SSH
```Bash
$ raspi-config
Interfacing options > Enable SSH
Network options > HostName > SensorX
```
8. Conectar por SSH
9. Copiar sensores.py al directorio home/pi
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
$ pip3 install w1thermsensor
$ pip3 install mh_z19
$ pip3 install Adafruit_DHT
$ pip3 install smbus
```
14. Set la zona horaria desde raspi-config

## Conexión de sensores
Habilitar la interface UART
```Bash
$ sudo nano /boot/config.txt
```
Add The following line at the end and reboot
```
enable_uart=1
```
Despues en raspi-config modificar lo siguiente:
```Bash
Interfacing options -> P6 Serial -> Logging NO -> Hardware YES
```

La conexión del sensor de CO2 como en la imagen
![Conexión](https://warehouse-camo.ingress.cmh1.psfhosted.org/5e69358ea376cf9c8460b74610e3cd2ca2f487f9/68747470733a2f2f63616d6f2e67697468756275736572636f6e74656e742e636f6d2f336364346331623438326561393032623765363664636131336434323630313933633833316136332f3638373437343730373333613266326636333631366436663265373136393639373436313735373336353732363336663665373436353665373432653633366636643266333133313332363136343335363636353334333136333338333236313331333633363337333136343332333833383332333033373330333333383334333133303339363333383338333633303633363332663336333833373334333733343337333033373333333336313332363633323636333733313336333933363339333733343336333133323634333633393336363433363331333633373336333533323634333733333337333433363636333733323336333533323635333733333333333333323635333633313336363433363331333736313336363633363635333633313337333733373333333236353336333333363636333636343332363633333330333236363333333433333336333333353333333433333334333236363333333033333338333333323333333833333333333333303333333133333334333236343333333633333338333633343333333233323634333633333333333333363334333633353332363433333331333333363333333433333334333236343333333733363333333333383336333433333339333633323333333733363332333333363333333233363336333633343332363533363631333733303336333533363337)
Pinout del sensor
![pinout](https://www.circuits.dk/wp-content/uploads/2017/06/CO2-sensor-MH-Z19-pinout.jpg)

La conexión del sensor de temperatura es como en la imagen pero los pines de señal de los 4 sensores van en GPIO2, GPIO3, GPIO4 y GPIO17
![temp_conexion](https://www.circuitbasics.com/wp-content/uploads/2015/12/How-to-Setup-the-DHT11-on-the-Raspberry-Pi-Three-pin-DHT11-Wiring-Diagram-1024x479.png)
El pinout es este
![temp_pin](https://www.circuitbasics.com/wp-content/uploads/2015/12/DHT11-Pinout-for-three-pin-and-four-pin-types-2-1024x742.jpg)

Para el sensor SHT30 habilitar el I2C desde raspi-config y conectar los pines SCL y SDA a las raspberry
![sht_pin](https://i.ibb.co/zHFF4P6/ndice.jpg)


## Iniciar el script
El script comienza atomáticamente con supervisord
1. Cambiar el AccesToken en sensores.py por el que da la dashboard para cada raspberry
2. Instalar supervisord
```Bash
$ sudo apt-get install supervisor
```
3. Configurar supervisord con el script
```Bash
$ cd /etc/supervisor/conf.d/
$ sudo nano sensores.conf
```
4. Agregar la configuración
```Python
[program:sensores]
directory = /home/pi/
#command = sudo python3 sensores.py
command = sudo python3 sensores_SHT30.py
user = root
password = raspberry
autosart = true
identifier = sensores
autorestart = true
startretries = 20
stdout_logfile=/var/log/supervisor/sensores.log
```

## Revisar 
En el servidor de Thingsboard se debe configurar los widgets que reciban el Topic del sensor y revisar que estén recibiendo datos. Incluso cuando los sensores están desconectados el módulo envía el timestamp y el porcentaje de memoria de la RP.

Revisar los logs en
```Bash
$ cd /var/log/supervisor/Program.log
```
