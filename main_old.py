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
    # os.system("Covid_Checker.exe")    # using this once ready to be .exe exported
    os.system("python main.py")       # using this while testing

def exception():
    # If QR not okay, will execute this
    print("The QR is not read correctly or something illegal is typed in.")  # prompt
    print("Check the input language and the keyboard for blocked keys.")     # prompt
    print("Try again or with different certificate.")                        # prompt
    print("Restarting...")                                                   # prompt
    os.system("PING -n 1 127.0.0.1>nul")                                    # wait time before restarting

# Abbreviation : country
CO = {'AD':'Andorra', 'AE':'United Arab Emirates', 'AT':'Austria', 'BE':'Belgium','BG':'Bulgaria', 'CH':'Switzerland',
      'CY':'Cyprus', 'CZ':'Czech Republic', 'DE':'Germany', 'DK':'Denmark', 'EE':'Estonia', 'ES':'Spain', 'FI':'Finland',
      'FR':'France', 'GE':'Georgia', 'GR':'Greece', 'HR':'Croatia', 'HU':'Hungary', 'IE':'Ireland', 'IS':'Iceland',
      'IT':'Italy', 'LI':'Liechtenstein','LT':'Lithuania', 'LU':'Luxembourg', 'LV':'Latvia', 'MA':'Morocco', 'MT':'Malta',
      'NL':'Netherlands', 'NO':'Norway','PL':'Poland', 'PT':'Portugal', 'RO':'Romania', 'SE':'Sweden', 'SG':'Singapore',
      'SI':'Slovenia', 'SK':'Slovakia', 'SM':'San Marino', 'UA':'Ukraine', 'VA':'Vatican','GB':'Great Britain'}
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
payload = getpass.getpass('Please, scan the QR on the certificate\nClose the window to quit\n').upper()  # waiting the user input

# trimming the prefix
payload = payload[4:]

# Decoding is done in steps for better documentation and debugging

# decode Base45 (with removed HC1: prefix)
try:
    decoded = base45.b45decode(payload)
except:
    exception()
    reset()

# decompress using zlib
try:
    decompressed = zlib.decompress(decoded)
except:
    exception()
    reset()

# decode COSE message (no signature verification done)
cose = CoseMessage.decode(decompressed)

# decode the CBOR encoded payload converting the information to readable json struct
whole = (json.dumps(cbor2.loads(cose.payload), ensure_ascii=False, indent=2, sort_keys=True, default=str))  # reliable
j_whole = json.loads(whole)

"""
"""
# Debugging in case of new json struct
print("Debugging...")
print("__________________________")
print(whole)
# print(j_whole['1'])
print("__________________________")
print(" ")
os.system("pause")


# Checking validity
def validity():
    today = datetime.today()
    # Forming the date to check by adding the days from the .ini file to the date from the cert
    if len(date_from) == 10:
        if k == "v":
            date = datetime.strptime(date_from, '%Y-%m-%d') + timedelta(days=15) + timedelta(days=vall)
        elif k == "r":
            date = datetime.strptime(date_from, '%Y-%m-%d') + timedelta(days=vall)
        elif k == "t":
            date = datetime.strptime(date_from, '%Y-%m-%d') + timedelta(days=vall)
    elif len(date_from) > 10:
        if k == "v":
            date = datetime.strptime(date_from[:10], '%Y-%m-%d') + timedelta(days=15) + timedelta(days=vall)
        elif k == "r":
            date = datetime.strptime(date_from[:10], '%Y-%m-%d') + timedelta(days=vall)
        elif k == "t":
            
            date = datetime.strptime(date_from[:10], '%Y-%m-%d') + timedelta(days=vall)
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
    print("Unique Certificate Identifier: " + str(j_whole['-260']['1']['r'][0]['ci']))
    for K, V in CO.items():
        if j_whole['1'] == K:
            print("Country: " + V)
    # print("Country: " + (j_whole['1']))
    validity()

# Vaccine cert
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
    print(".:::::::::::::::::::::::::::::::::::ЦИФРОВ COVID СЕРТИФИКАТ НА ЕС:::::::::::::::::::::::::::::::::::.")
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

# Determining the kind of cert and error handling in case it fails to parse it correctly
dick = j_whole['-260']['1']  # the dic with the needed information for the funcs above
for k, v in dick.items():
    if k == "r":       # recovery
        if v is None:  # if empty will continue to the next sub-dic
            continue
        # Building variables
        date_from = j_whole['-260']['1']['r'][0]['df']
        val = open("val_rec.ini", "r")  # Opens it in read mode
        vall = list(val)                # Converting data to list
        vall = int(vall[0])             # Taking the first (and only) item and convert it to int
        val.close()                     # Closes the file
        try:
            sick_cert()  # calling the right func
        except:
            exception()
            reset()
    elif k == "v":  # vaccine
        if v is None:
            continue
        date_from = j_whole['-260']['1']['v'][0]['dt']
        val = open("val_vac.ini", "r")  # Opens it in read mode
        vall = list(val)                 # Converting data to list
        vall = int(vall[0])              # Taking the first (and only) item and convert it to int
        val.close()                      # Closes the file
        try:
            vac_cert()
        except:
            exception()
            reset()
    elif k == "t":  # test cert
        if v is None:
            continue
        date_from = j_whole['-260']['1']['t'][0]['sc']
        val = open("val_test.ini", "r")  # Opens it in read mode
        vall = list(val)                 # Converting data to list
        vall = int(vall[0])              # Taking the first (and only) item and convert it to int
        val.close()                      # Closes the file
        try:
            test_cert()
        except:
            exception()
            reset()
    else:
        print("New or unsupported format. Please contact development team.")


"""
# Opening the ini file
val = open("val_vacc.ini", "r")  # Opens it in read mode
vall = list(val)                 # Converting data to list
vall = int(vall[0])              # Taking the first (and only) item and convert it to int
val.close()                      # Closes the file

val = open("val_rec.ini", "r")  # Opens it in read mode
vall = list(val)                # Converting data to list
vall = int(vall[0])             # Taking the first (and only) item and convert it to int
val.close()                     # Closes the file

val = open("val_test.ini", "r")  # Opens it in read mode
vall = list(val)                 # Converting data to list
vall = int(vall[0])              # Taking the first (and only) item and convert it to int
val.close()                      # Closes the file
"""