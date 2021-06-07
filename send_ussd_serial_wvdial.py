#!/usr/bin/python
# coding: utf-8

import time, sys
import serial
from timeit import default_timer as timer

"""
Date: Thu  3 Jun 23:34:12 BST 2021
Develop: bryan@gridshield.net
Ticket: 31777, 32373
"""

verbose = False
ussd = False
port = "/dev/ttyACM1"
baud = 9600
##baud = 115200 
timeout_serial = 10
##ussd = serial.Serial("/dev/ttyACM1",  9600, timeout=10)

def connect():

    global ussd, port, baud, timeout_serial
    start = timer()
    try:
        ussd = serial.Serial(port, baud, timeout = timeout_serial )
        print_verbose("OK", "Inicaliza Modem")
    except Exception as e:
	end = timer()
	time_exec = end - start
        print "CRITICAL - Error de conexion: " +  str(e) + " Duracion de conexion: " + str(round(time_exec,6)) + "seg | time=" + str(round(time_exec,6))
        sys.exit(2)

def print_verbose( vtype, text):
	global verbose

	if not(verbose):
	        return
	toprint = ''
	if vtype == "OK":
	        toprint = "[+] " + text
	elif vtype == "ERROR":
	        toprint = "[-] Error: " + text
	elif vtype == "REMOVE":
	        toprint = "[-] " + text
	elif vtype == "WARNING":
	        toprint = "[*] Warning: " + text
	elif vtype == "INFO":
	        toprint = "[*] " + text
	elif vtype == "BLANK":
	        toprint = "" + text
	elif vtype == "TAB":
	        toprint = "\t" + text

	print toprint

def writefile(datalines, name):
	filename = "/var/lib/gms/plugins/pax/beneficios/" + str(name)
	datafile = open(filename, 'w')
	datafile.writelines(datalines)
	datafile.close()

def getSaldo(proof):

	import re
	saldo = 'None'
	try:
	        value = re.search(r'CUSD:\s+.*?\"Tu\s+saldo\s+es\s+(.*?)\s+colones(.*?)\"', proof, re.MULTILINE | re.DOTALL)
	        if value == None:
			return saldo

	        else:
	                saldo = value.group(1)
	                return saldo

	        return saldo

	except Exception, e:
	        return saldo

def returnNagios(saldo, time_exec):

    if ( saldo == 'None'):
        print "CRITICAL - No se encontro saldo disponible para la consulta de Beneficios. Saldo Disponible: "  + str(saldo)  + " Colones. Duracion de la consulta: " +  str(time_exec)  + "seg | time=" + str(time_exec)
        sys.exit(2)
    else:
        print "OK - Se encontro el saldo disponible para la consulta de Beneficios. Saldo Disponible: " + str(saldo)  +  " Colones. Duracion de la consulta: " +  str(time_exec)  + "seg | time=" + str(time_exec)
        sys.exit(0)

def sendUSSDCodeBeneficios(ussd):

	print_verbose("OK", "Envia codigo consulta Saldo Beneficios - Prepago")
        ussd.write(b'ATZ\r')
        time.sleep(0.1)
        ussd.write(b'AT+CSCS="GSM"\r')
        time.sleep(0.1)
        ussd.write(b'AT+CUSD=1,"*888*1*1#",15\r')
        time.sleep(4)

def main():
    global ussd

    try:
        start = timer()
        connect()
	sendUSSDCodeBeneficios(ussd)
        response =  ussd.read(2048)
        ##writefile(response.replace('\r',''), 'response_code_saldo.txt')
	saldo = getSaldo( response.replace('\r','') )
        print_verbose("OK", "Saldo Prepago es: " + str(saldo) )
        print_verbose("OK", "Response Kolbi3g(USSD): \n" +  "*** Inicio de Respuesta ***\n" + str(response) + "\n*** Fin de Respuesta ***" )
        ussd.close()
        print_verbose("OK","Cierra conexion")
        end = timer()
        time_exec = end - start
        returnNagios(saldo, round(time_exec, 5))

    except Exception as e:
    ##finally:
        print "CRITICAL - Error: " + str(e)
        ussd.close()
        sys.exit(2)
main()
