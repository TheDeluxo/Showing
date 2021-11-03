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

def reset():  # restarts the whole program
    os.system("Covid_Checker.exe")    # using this once ready to be .exe exported
    # os.system("python main.py")       # using this while testing

# Countries and codes
CO = {'AD':'Andorra', 'AE':'United Arab Emirates', 'AT':'Austria', 'BE':'Belgium','BG':'Bulgaria', 'CH':'Switzerland',
      'CY':'Cyprus', 'CZ':'Czech Republic', 'DE':'Germany', 'DK':'Denmark', 'EE':'Estonia', 'ES':'Spain', 'FI':'Finland',
      'FR':'France', 'GE':'Georgia', 'GR':'Greece', 'HR':'Croatia', 'HU':'Hungary', 'IE':'Ireland', 'IS':'Iceland',
      'IT':'Italy', 'LI':'Liechtenstein','LT':'Lithuania', 'LU':'Luxembourg', 'LV':'Latvia', 'MA':'Morocco', 'MT':'Malta',
      'NL':'Netherlands', 'NO':'Norway','PL':'Poland', 'PT':'Portugal', 'RO':'Romania', 'SE':'Sweden', 'SG':'Singapore',
      'SI':'Slovenia', 'SK':'Slovakia', 'SM':'San Marino', 'UA':'Ukraine', 'VA':'Vatican'}
"""
# Walking over CO for test
for k, v in CO.items():
    print("Code: " + k + " = Country: " + v)
# os.system("pause")
"""
# First resetting the screen
os.system("cls")
os.system("color 0f")
print(".:::::::::::::::::::::::::::::::::::EU DIGITAL COVID CERTIFICATE::::::::::::::::::::::::::::::::::::.")
print(".:::::::::::::::::::::::::::::::::::ЦИФРОВ COVID СЕРТИФИКАТ НА ЕС:::::::::::::::::::::::::::::::::::.")

# Invisible input
payload = getpass.getpass('Please, scan the QR on the certificate\nClose the window to quit\n')  # waiting the user input

# trimming the prefix
payload = payload[4:]

# Decoding is done in steps for better documentation and debugging

# decode Base45 (with removed HC1: prefix)
try:
    decoded = base45.b45decode(payload)
except:
    # If QR not okay, will execute this
    print("The QR is not read correctly or something illegal is typed in.\nCheck the input language or 'Caps lock'.") # prompt
    print("Restarting...")                # prompt
    os.system("PING -n 7 127.0.0.1>nul")  # wait time
    reset()

# decompress using zlib
try:
    decompressed = zlib.decompress(decoded)
except:
    # If QR not okay, will execute this
    print("The QR is not read correctly or something illegal is typed in.\nCheck the input language or 'Caps lock'.") # prompt
    print("Restarting...")                # prompt
    os.system("PING -n 7 127.0.0.1>nul")  # wait time
    reset()

# decode COSE message (no signature verification done)
cose = CoseMessage.decode(decompressed)

# decode the CBOR encoded payload converting the information to readable json struct
whole = (json.dumps(cbor2.loads(cose.payload), ensure_ascii=False, indent=2, sort_keys=True, default=str))  # reliable
j_whole = json.loads(whole)

"""
# Debugging in case of new json struct
print("Debugging...")
print("__________________________")
print(whole)
# print(j_whole['1'])
print("__________________________")
print(" ")
os.system("pause")
"""

# Opening the ini file
f = open("validity.ini", "r") # Opens it in read mode
ff = list(f)              # Converting data to list
ff = int(ff[0])           # Taking the first (and only) item and convert it to int
f.close()                 # Closes the file

# Checking validity
def validity():
    # Forming the date to check by adding the days from the .ini file to the date from the cert
    if len(date_from) == 10:
        date = datetime.strptime(date_from, '%Y-%m-%d') + timedelta(days=ff)
    elif len(date_from) > 10:
        date = datetime.strptime(date_from[:10], '%Y-%m-%d') + timedelta(days=ff)  # trimming the unnecessary
    # Comparing the date of expire against today
    if today < date:  # Valid cert
        # Doing it like that so no additional .bat files are needed
        os.system("color 20")
        os.system('@echo off && chcp 65001>nul && start /b /wait MessageBox.exe "The certificate is valid!" "Information">nul')
        reset()
    else:  # Invalid cert
        # Doing it like that so no additional .bat files are needed
        os.system("color c0")
        os.system('@echo off && chcp 65001>nul && start /b /wait MessageBox.exe "The certificate is invalid!" "Attention!" /i:E>nul')
        reset()

# Recovery cert
def sick_cert():
    os.system("cls")
    print(".:::::::::::::::::::::::::::::::::::EU DIGITAL COVID CERTIFICATE::::::::::::::::::::::::::::::::::::.")
    print(".:::::::::::::::::::::::::::::::::::ЦИФРОВ COVID СЕРТИФИКАТ НА ЕС:::::::::::::::::::::::::::::::::::.")
    print("")
    print(".:::::::::::::::::::::::::::::::::::::::Recovery certificate::::::::::::::::::::::::::::::::::::::::.")
    print("Certificate information: ")
    print("Native Name: " + str(j_whole['-260']['1']['nam']['gn']) + " " + str(j_whole['-260']['1']['nam']['fn']))
    print("EN Name: "     + str(j_whole['-260']['1']['nam']['gnt']) + " " + str(j_whole['-260']['1']['nam']['fnt']))
    print("Valid from:  " + str(j_whole['-260']['1']['r'][0]['df']))
    print("Valid until: " + str(j_whole['-260']['1']['r'][0]['du']))
    print("Unique Certificate Identifier: " + str(j_whole['-260']['1']['r'][0]['ci'][9:]))
    for K, V in CO.items():
        if j_whole['1'] == K:
            print("Country: " + V)
    # print("Country: " + (j_whole['1']))
    validity()

# Vacc cert
def vac_cert():
    os.system("cls")
    print(".:::::::::::::::::::::::::::::::::::EU DIGITAL COVID CERTIFICATE::::::::::::::::::::::::::::::::::::.")
    print(".:::::::::::::::::::::::::::::::::::ЦИФРОВ COVID СЕРТИФИКАТ НА ЕС:::::::::::::::::::::::::::::::::::.")
    print(" ")
    print(".::::::::::::::::::::::::::::::::::::::Vaccination certificate::::::::::::::::::::::::::::::::::::::.")
    print("Certificate information: ")
    print("Native Name: " + str(j_whole['-260']['1']['nam']['gn'] + " "  + str(j_whole['-260']['1']['nam']['fn'])))
    print("EN Name: "     + str(j_whole['-260']['1']['nam']['gnt'] + " " + str(j_whole['-260']['1']['nam']['fnt'])))
    print("Date Issued: " + str(j_whole['-260']['1']['v'][0]['dt']))
    print("Unique Certificate Identifier: " + j_whole['-260']['1']['v'][0]['ci'])
    for K, V in CO.items():
        if j_whole['1'] == K:
            print("Country: " + V)
    # print("Country: " + (j_whole['1']))
    validity()

# Test cert
def test_cert():
    os.system("cls")
    print(".:::::::::::::::::::::::::::::::::::EU DIGITAL COVID CERTIFICATE::::::::::::::::::::::::::::::::::::.")
    print(" .:::::::::::::::::::::::::::::::::::ЦИФРОВ COVID СЕРТИФИКАТ НА ЕС:::::::::::::::::::::::::::::::::::.")
    print(" ")
    print(".:::::::::::::::::::::::::::::::::::::::::Test certificate::::::::::::::::::::::::::::::::::::::::::.")
    print("Certificate information: ")
    print("Native Name: " + str(j_whole['-260']['1']['nam']['gn']) + " " + str(j_whole['-260']['1']['nam']['fn']))
    print("EN Name: "     + str(j_whole['-260']['1']['nam']['gnt']) + " " + str(j_whole['-260']['1']['nam']['fnt']))
    print("Date Issued: " + str(j_whole['-260']['1']['t'][0]['sc']))
    print("Unique Certificate Identifier: " + j_whole['-260']['1']['t'][0]['ci'])
    for K, V in CO.items():
        if j_whole['1'] == K:
            print("Country: " + V)
    # print("Country: " + (j_whole['1']))
    validity()

# Determining the kind of cert
dick = j_whole['-260']['1']  # the dic with the needed information for the func above
for k, v in dick.items():
    if k == "r": # recovery
        if v is None:  # if empty will continue to the next sub-dic
            continue
        # building variables
        date_from = j_whole['-260']['1']['r'][0]['df']
        today = datetime.today()
        # calling the right func
        sick_cert()
    elif k == "v": # vaccine
        if v is None:
            continue
        # building variables
        date_from = j_whole['-260']['1']['v'][0]['dt']
        today = datetime.today()
        # calling the right func
        vac_cert()
    elif k == "t": # test cert
        if v is None:
            continue
        # building variables
        date_from = j_whole['-260']['1']['t'][0]['sc']
        today = datetime.today()
        # calling the right func
        test_cert()

