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

4. Agregar la red al final
```Bash
network={
    ssid="maticas_net"
    psk="yatusabe"
}
```
5. Probar con ifconfig o ping que está conectado a la red
6. Activar el SSH
```Bash
$ raspi-config
Interfacing options
Enable SSH
Network options
HostName
SensorX
```
7. Conectar por SSH
8. Copiar sensores.py al directorio home/pi
9. Remover python 2.7
```Bash
$ sudo apt-get remove python2.7
$ sudo apt-get autoremove
```
10. Instalar python 3.7.8
```Bash
$ sudo apt-get update
$ sudo apt-get install -y build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev tar wget vim
$ wget https://www.python.org/ftp/python/3.8.3/Python-3.8.3.tgz
$ sudo tar zxf Python-3.8.3.tgz
$ cd Python-3.8.3
$ sudo ./configure --enable-optimizations
$ sudo make -j 4
$ sudo make altinstall
$ echo "alias python=/usr/local/bin/python3.8" >> ~/.bashrc
$ source ~/.bashrc
```


## Conexión de sensores


## Iniciar el script


## Revisar 
En el servidor de Thingsboard se debe configurar los widgets que reciban el Topic del sensor y revisar que estén recibiendo datos. Incluso cuando los sensores están desconectados el módulo envía el timestamp