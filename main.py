#! /usr/bin/env python3
import json
import zlib
import os
import sys
import getpass
from datetime import datetime, timedelta
import base45
import cbor2
from cose.messages import CoseMessage

os.system("cls")
os.system("color 0f")
print(" .::::::::::::::::::::::::::::::::::::::EU DIGITAL COVID CERTIFICATE:::::::::::::::::::::::::::::::::::::::.")
print(" .::::::::::::::::::::::::::::::::::::::ЦОФРОВ COVID СЕРТИФИКАТ НА ЕС::::::::::::::::::::::::::::::::::::::.")


print('Please, scan the QR\n')
print('Or type "exit" to quit\n')
payload = input()
if payload.lower() == "exit":
    sys.exit()

# payload = getpass.getpass(prompt = 'Please, scan the QR and wait a bit...\n', stream = None)
# payload = str(payload)
# print(payload)
# os.system("pause")

payload = payload[4:]

# Sick
# payload = "NCFOXN*TS0BI$ZDYSH$PJ6RQPM3 RF:D4+Z8-36HD7-TM5V4I/QI9C+MH+W2RAC/GPWBILC9%FAGUUR-SCG1CSQ6U7SSQY%SVJ55M8N:4*J5N3I4-2Q093TKG9J+30G9A450:IU$*SJAK9B9EEDG%8G%85QNG.8W%89B9H*KJ2KX2M093/24G*L:%5+9D.XIKXB8UJ06J9UBSVAXCIF4LEIIPBJ NI5VA81K0ECM8CXVDC8C 1J5OI9YI:8DBLC+NDC%QE2KI7JSTNB95WAM/ROUK1H%55:NH-S8VGCPEV*PB86QQOI%KXYNDZCG2F.7B7D0ZLO0I1 O2LV9586COO6443WE970R B4JBPC98AEBVL$UK*5GXPC6LFND9AQC$UK5RCV9NA+H.8LP2DS22XCNQ+MN/QP9QE8QHOO$+K8MO-TJD6L81FYUR:*IZQ8//LSDU4O3/1DGXRPOVVZT:+JPVBGCPS+E%BA$R1%2S84A$2IQ898%S:0FBSK G7KP2:.AKH3:H6/AWF50D8WK0"
# vac
# payload = "NCFOXN*TS0BI$ZDYSH$PJ6RQPM3 RF:D4+ A-36HD7-TMAZ4H4QI9CGJ9RUIRAC/GPWBILC9GGBYPLR-SCG1CSQ6U7SSQY%SVJ55M8N:4.TL4WSN2EJ/1S65434IXPV44S:577I$*SJAK9B92FF9B9LW4G%89-8CNNM3LW1HVD9B.OD4OYGFO-O%Z8JH1PCDJ*3TFH2V4IE9MIHJ6W48UK.GCY0$2PH/MIE9WT0K3M9UVZSVV*001HW%8UE9.955B9-NT0 2$$0X4PCY0+-CVYCRMTB*05*9O%0HJP7NVDEBK3JPZ0I2U9-87LPMIH-O92UQ-C1KV9JBM$DHXG0+NOJXU0T9QK90VLT7O32TVVH3REECFN%GF-2P253ZCK$B9LF781YV3QZ94JBCD9AQC$UK5RCK4GBLEH-B/GG.8L:3DIQCOZ9MCHIUJ6/3ACMQ+MN/QP9QE8Q POMMU50EUGP819C LEX2Q.TORE7/O0OTPY2ZL230OSWP*6QB/7C9FOSJ36KE:A3RD1XRM:OH/PQ$GA432CUKW13ZKD/LADLBTRJLPQ5MU I3$I"

# decode Base45 (remove HC1: prefix)
decoded = base45.b45decode(str(payload))

# decompress using zlib
decompressed = zlib.decompress(decoded)
# decode COSE message (no signature verification done)
cose = CoseMessage.decode(decompressed)
# decode the CBOR encoded payload and print as json

whole = (json.dumps(cbor2.loads(cose.payload),ensure_ascii=False, indent=2))
j_whole = json.loads(whole)

# Opening the config file in read mode taking the value as var.
f = open("time.ini", "r")
ff = list(f)
ff = int(ff[0])
f.close()

# Checking validity
def validity():
    date = datetime.strptime(date_from, '%Y-%m-%d') + timedelta(days=ff)
    if today < date:
        os.system("color 20")
        os.system('@echo off && chcp 65001>nul && start /b /wait MessageBox.exe "The certificate is valid!" "Information"')
        os.system("main.py")
    else:
        os.system("color c0")
        os.system('@echo off && chcp 65001>nul && start /b /wait MessageBox.exe "The certificate is invalid!" "Attention!" /i:E')
        os.system("main.py")

def sick():
    os.system("cls")
    print(" .::::::::::::::::::::::::::::::::::::::EU DIGITAL COVID CERTIFICATE:::::::::::::::::::::::::::::::::::::::.")
    print(" .::::::::::::::::::::::::::::::::::::::ЦОФРОВ COVID СЕРТИФИКАТ НА ЕС::::::::::::::::::::::::::::::::::::::.")
    print("")
    print(" .::::::::::::::::::::::::::::::::::::::::::Recovery certificate:::::::::::::::::::::::::::::::::::::::::::.")
    print("Certificate information: ")
    print("BG Name: " + str(j_whole['-260']['1']['nam']['gn']) + " " + str(j_whole['-260']['1']['nam']['fn']))
    print("EN Name: " + str(j_whole['-260']['1']['nam']['gnt']) + " " + str(j_whole['-260']['1']['nam']['fnt']))
    print("Valid from:  " + str(j_whole['-260']['1']['r'][0]['df']))
    print("Valid until: " + str(j_whole['-260']['1']['r'][0]['du']))
    print("Unique Certificate Identifier: " + str(j_whole['-260']['1']['r'][0]['ci'][9:]))
    validity()

def vac():
    os.system("cls")
    print(" .::::::::::::::::::::::::::::::::::::::EU DIGITAL COVID CERTIFICATE:::::::::::::::::::::::::::::::::::::::.")
    print(" .::::::::::::::::::::::::::::::::::::::ЦОФРОВ COVID СЕРТИФИКАТ НА ЕС::::::::::::::::::::::::::::::::::::::.")
    print("")
    print(" .:::::::::::::::::::::::::::::::::::::::::Vaccination certificate:::::::::::::::::::::::::::::::::::::::::.")
    print("Certificate information: ")
    print("BG Name: " + str(j_whole['-260']['1']['nam']['gn']) + " " + str(j_whole['-260']['1']['nam']['fn']))
    print("EN Name: " + str(j_whole['-260']['1']['nam']['gnt']) + " " + str(j_whole['-260']['1']['nam']['fnt']))
    print("Date Issued: " + str(j_whole['-260']['1']['v'][0]['dt']))
    print("Unique Certificate Identifier: " + j_whole['-260']['1']['v'][0]['ci'][9:])
    validity()

# Determining the kind of cert
dick = j_whole['-260']['1']
for k, v in dick.items():
    # print('Key: ' + k)
    if k == "r":
        # building variables
        date_from = j_whole['-260']['1']['r'][0]['du']
        today = datetime.today()
        # calling the right func
        sick()
    elif k == "v":
        # building variables
        date_from = j_whole['-260']['1']['v'][0]['dt']
        today = datetime.today()
        # calling the right func
        vac()

