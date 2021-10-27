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

# First resetting the screen
os.system("cls")
os.system("color 0f")
print(" .::::::::::::::::::::::::::::::::::::::EU DIGITAL COVID CERTIFICATE:::::::::::::::::::::::::::::::::::::::.")
print(" .::::::::::::::::::::::::::::::::::::::ЦОФРОВ COVID СЕРТИФИКАТ НА ЕС::::::::::::::::::::::::::::::::::::::.")

"""
# Visible input
print('Please, scan the QR\n')
print('Or type "exit" to quit\n')
payload = input() # waiting the user input
# if user type in "exit" will terminate the script and the window
if payload.lower() == "exit": # case insensitive
     sys.exit()
"""

# Invisible input
# waiting the user input
payload = getpass.getpass('Please, scan the QR and wait a bit...\nOr type "exit" to quit\n')
# if user type in "exit" will terminate the script and the window
if payload.lower() == "exit": # case insensitive
     sys.exit()

payload = payload[4:]

# decode Base45 (remove HC1: prefix)
decoded = base45.b45decode(str(payload))

# decompress using zlib
try:
    decompressed = zlib.decompress(decoded)
except:
    # If QR not okay, will execute this
    print("The QR is not read correctly or something illegal is typed in.")
    print("Restarting...")
    os.system("PING -n 7 127.0.0.1>nul")
    os.system("start.bat")
# decode COSE message (no signature verification done)
cose = CoseMessage.decode(decompressed)
# decode the CBOR encoded payload and print as json

# Converting the information to readable json struct
whole = (json.dumps(cbor2.loads(cose.payload),ensure_ascii=False, indent=2))
j_whole = json.loads(whole)

# Opening the ini file
f = open("time.ini", "r") # Opens it in read mode
ff = list(f)              # Converting data to list
ff = int(ff[0])           # Taking the first (and only) item and convert it to int
f.close()                 # Closes the file

# Checking validity
def validity():
    # Forming the date to check by adding the days from the .ini file to the date from the cert
    date = datetime.strptime(date_from, '%Y-%m-%d') + timedelta(days=ff)
    # Comparing the date to check with today
    if today < date:
        # Doing it like that so no additional .bat files are needed
        os.system("color 20")
        os.system('@echo off && chcp 65001>nul && start /b /wait MessageBox.exe "The certificate is valid!" "Information"')
        os.system("main.py")
    else:
        # Doing it like that so no additional .bat files are needed
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

