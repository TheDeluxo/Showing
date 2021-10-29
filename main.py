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
print(" .::::::::::::::::::::::::::::::::::::::ЦИФРОВ COVID СЕРТИФИКАТ НА ЕС::::::::::::::::::::::::::::::::::::::.")

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
try:
    decoded = base45.b45decode(payload)
except:
    # If QR not okay, will execute this
    print("The QR is not read correctly or something illegal is typed in.\nCheck the input language.") # prompt
    print("Restarting...")                                                  # prompt
    os.system("PING -n 7 127.0.0.1>nul")                                    # wait time
    os.system("start.bat")                                                  # restart the whole thing

# decompress using zlib
try:
    decompressed = zlib.decompress(decoded)
except:
    # If QR not okay, will execute this
    print("The QR is not read correctly or something illegal is typed in.\nCheck the input language.") # prompt
    print("Restarting...")                                                  # prompt
    os.system("PING -n 7 127.0.0.1>nul")                                    # wait time
    os.system("start.bat")                                                  # restart the whole thing

# decode COSE message (no signature verification done)
cose = CoseMessage.decode(decompressed)

# decode the CBOR encoded payload converting the information to readable json struct
whole = (json.dumps(cbor2.loads(cose.payload),ensure_ascii=False, indent=2))
j_whole = json.loads(whole)

# Opening the ini file
f = open("time.ini", "r") # Opens it in read mode
ff = list(f)              # Converting data to list
ff = int(ff[0])           # Taking the first (and only) item and convert it to int
f.close()                 # Closes the file

def ver_check():
    print("")
    print("__________________________")
    print("Debugging: ")
    print("Current version: " + ver)
    print("__________________________")

# Checking validity
def validity():
    # json version check. Should be removed once finished
    ver_check()
    # Forming the date to check by adding the days from the .ini file to the date from the cert
    # Dealing with the differences in the struct versions
    if ver == "1.3.0":
        date = datetime.strptime(date_from, '%Y-%m-%d') + timedelta(days=ff)
    elif ver == "1.0.0":
        date = datetime.strptime(date_from[:10], '%Y-%m-%d') + timedelta(days=ff)  # trimming the unnecessary
    # Comparing the date of expire against today
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
    print(" .::::::::::::::::::::::::::::::::::::::ЦИФРОВ COVID СЕРТИФИКАТ НА ЕС::::::::::::::::::::::::::::::::::::::.")
    print("")
    print(" .::::::::::::::::::::::::::::::::::::::::::Recovery certificate:::::::::::::::::::::::::::::::::::::::::::.")
    print("Certificate information: ")
    print("BG Name: " + str(j_whole['-260']['1']['nam']['gn']) + " "  + str(j_whole['-260']['1']['nam']['fn']))
    print("EN Name: " + str(j_whole['-260']['1']['nam']['gnt']) + " " + str(j_whole['-260']['1']['nam']['fnt']))
    print("Valid from:  " + str(j_whole['-260']['1']['r'][0]['df']))
    print("Valid until: " + str(j_whole['-260']['1']['r'][0]['du']))
    print("Unique Certificate Identifier: " + str(j_whole['-260']['1']['r'][0]['ci'][9:]))
    print("Country: " + j_whole['-260']['1']['r'][0]['co'])
    validity()

def vac():
    os.system("cls")
    print(" .::::::::::::::::::::::::::::::::::::::EU DIGITAL COVID CERTIFICATE:::::::::::::::::::::::::::::::::::::::.")
    print(" .::::::::::::::::::::::::::::::::::::::ЦИФРОВ COVID СЕРТИФИКАТ НА ЕС::::::::::::::::::::::::::::::::::::::.")
    print("")
    print(" .:::::::::::::::::::::::::::::::::::::::::Vaccination certificate:::::::::::::::::::::::::::::::::::::::::.")
    print("Certificate information: ")
    print("BG Name: " + str(j_whole['-260']['1']['nam']['gn']) + " "  + str(j_whole['-260']['1']['nam']['fn']))
    print("EN Name: " + str(j_whole['-260']['1']['nam']['gnt']) + " " + str(j_whole['-260']['1']['nam']['fnt']))
    print("Date Issued: " + str(j_whole['-260']['1']['v'][0]['dt']))
    print("Unique Certificate Identifier: " + j_whole['-260']['1']['v'][0]['ci'][9:])
    print("Country: " + j_whole['-260']['1']['v'][0]['co'])
    validity()

# Determining the kind of cert
dick = j_whole['-260']['1']
for k, v in reversed(dick.items()):  # reverse walk through because of the "ver" position
    #print("current k = " + str(k) + " current v = " + str(v))
    if k == "ver":
        ver = v
    if k == "r": # recovery
        #print("current k = " + str(k) + " current v = " + str(v))
        if v == "null":
            continue
        # building variables
        date_from = j_whole['-260']['1']['r'][0]['du']
        today = datetime.today()
        # calling the right func
        sick()
    elif k == "v": # vaccine
        # building variables
        date_from = j_whole['-260']['1']['v'][0]['dt']
        today = datetime.today()
        # calling the right func
        vac()

