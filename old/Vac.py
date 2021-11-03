#! /usr/bin/env python3
import json
import sys
import zlib
import os
import getpass


import base45
import cbor2
from cose.messages import CoseMessage


payload = input('Please, scan the QR\n')
os.system("cls")
# payload = getpass.getpass('Please, scan the QR and wait a bit\n')

payload = payload[4:]

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
# print(j_whole['-260']['1']['v'][0]['ci'])
print("BG Name: " + str(j_whole['-260']['1']['nam']['gn']) + " " + str(j_whole['-260']['1']['nam']['fn']))
print("EN Name: " + str(j_whole['-260']['1']['nam']['gnt']) + " " + str(j_whole['-260']['1']['nam']['fnt']))
print("Date Issued: " + str(j_whole['-260']['1']['v'][0]['dt']))