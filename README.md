# Envió de Codigos USSD
Monitoreo que utiliza un modem(Datacard), para hacer envió de codigos USSD usando la red de GSM

Este proceso se utilizo Raspbian

```
root@raspberrypi:~# lsb_release -a
No LSB modules are available.
Distributor ID:	Raspbian
Description:	Raspbian GNU/Linux 10 (buster)
Release:	10
Codename:	buster


```

## Paqueteria

* []() apt-get install usb-modeswitch wvdial ppp
* []() apt-get install minicom python-serial

## Configuración wvdial

* []() Copiar la configuración de etc/wvdial.conf en /etc/wvdial.conf
* []() Copiar la configuración de etc/network/interfaces.d/ppp0 en  /etc/network/interfaces.d/ppp0
* []() Copiar la configuración  etc/rc.local en /etc/rc.local

## Ejecución

```
root@raspberrypi:/home/pi# python send_ussd_serial_wvdial.py
OK - Se encontro el saldo disponible para la consulta de Beneficios. Saldo Disponible: 966.9 Colones. Duracion de la consulta: 14.22925seg | time=14.22925

```

## Para pruebas manuales

```
root@raspberrypi:/home/pi# minicom -b 9600 -D /dev/ttyACM1
```
