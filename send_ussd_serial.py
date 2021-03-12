import time
import serial

##ussd = serial.Serial("/dev/ttyACM1",  115200, timeout=10)
ussd = serial.Serial("/dev/ttyUSB1",  115200, timeout=10)
try:
    print("Inicaliza Modem..\n")
    ussd.write(b'ATZ\r')
    time.sleep(0.5)
    ussd.write(b'AT+CSCS=?\r')
    time.sleep(0.1)
    ussd.write(b'AT+CSCS="GSM"\r')
    time.sleep(0.1)
    ussd.write(b'AT+CUSD=1\r')
    time.sleep(0.1)
    ussd.write(b'AT+CUSD=1,"*888*1*1#",15\r')
    time.sleep(0.1)
    ##ussd.write(b'AT+CUSD=1,"1",15\r')
    ##time.sleep(5)
    ##ussd.write(b'AT+CUSD=1,"1",15\r')
    ##time.sleep(5)
    ##ussd.write(b'AT+CUSD=0\r')
    ##time.sleep(0.5)
    response =  ussd.read(2048)
    print str(response)
finally:
    print("Cierra conexion\n")
    ussd.close()
