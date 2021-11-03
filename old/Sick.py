#! /usr/bin/env python3
import json
import sys
import zlib
import os
import getpass
from datetime import datetime, timedelta


import base45
import cbor2
from cose.messages import CoseMessage


payload = input('Please, scan the QR\n')
#os.system("cls")
# payload = getpass.getpass('Please, scan the QR and wait a bit\n')

payload = payload[4:]

# payload = "NCFOXN*TS0BI$ZDYSH$PJ6RQPM3 RF:D4+Z8-36HD7-TM5V4I/QI9C+MH+W2RAC/GPWBILC9%FAGUUR-SCG1CSQ6U7SSQY%SVJ55M8N:4*J5N3I4-2Q093TKG9J+30G9A450:IU$*SJAK9B9EEDG%8G%85QNG.8W%89B9H*KJ2KX2M093/24G*L:%5+9D.XIKXB8UJ06J9UBSVAXCIF4LEIIPBJ NI5VA81K0ECM8CXVDC8C 1J5OI9YI:8DBLC+NDC%QE2KI7JSTNB95WAM/ROUK1H%55:NH-S8VGCPEV*PB86QQOI%KXYNDZCG2F.7B7D0ZLO0I1 O2LV9586COO6443WE970R B4JBPC98AEBVL$UK*5GXPC6LFND9AQC$UK5RCV9NA+H.8LP2DS22XCNQ+MN/QP9QE8QHOO$+K8MO-TJD6L81FYUR:*IZQ8//LSDU4O3/1DGXRPOVVZT:+JPVBGCPS+E%BA$R1%2S84A$2IQ898%S:0FBSK G7KP2:.AKH3:H6/AWF50D8WK0"

print("Certificate information: ")

# decode Base45 (remove HC1: prefix)
decoded = base45.b45decode(str(payload))

# decompress using zlib
decompressed = zlib.decompress(decoded)
# decode COSE message (no signature verification done)
cose = CoseMessage.decode(decompressed)
# decode the CBOR encoded payload and print as json

whole = (json.dumps(cbor2.loads(cose.payload),ensure_ascii=False, indent=2))
j_whole = json.loads(whole)
print(whole)
# print(j_whole['-260']['1']['r'][0]['ci'][9:])
print("BG Name: " + str(j_whole['-260']['1']['nam']['gn']) + " " + str(j_whole['-260']['1']['nam']['fn']))
print("EN Name: " + str(j_whole['-260']['1']['nam']['gnt']) + " " + str(j_whole['-260']['1']['nam']['fnt']))
print("Valid from:  " + str(j_whole['-260']['1']['r'][0]['df']))
print("Valid until: " + str(j_whole['-260']['1']['r'][0]['du']))
print("Unique Certificate Identifier: " + j_whole['-260']['1']['r'][0]['ci'][9:])

# print(datetime.today().strftime('%Y-%m-%d'))

# Opening the config file in read mode taking the value as var.
f = open("time.ini", "r")
ff = list(f)
ff = int(ff[0])
f.close()

# building variables
date_from = j_whole['-260']['1']['r'][0]['du']
today = datetime.today()

# Checking validity
date = datetime.strptime(date_from, '%Y-%m-%d') + timedelta(days=ff)
print(date)
if today < date:
    os.system("color 20")
    os.system('@echo off && chcp 65001>nul && start /b /wait MessageBox.exe "The certificate is valid!" "Information"')
    os.system("main.py")
else:
    os.system("color c0")
    os.system('@echo off && chcp 65001>nul && start /b /wait MessageBox.exe "The certificate is invalid!" "Attention!" /i:E')
    os.system("main.py")

