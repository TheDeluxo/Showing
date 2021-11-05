#! /usr/bin/env python3
import json
import zlib
import os
import sys
import getpass
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
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
    os.system("PING -n 4 127.0.0.1>nul")                                    # wait time before restarting

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

"""
# test payloads
# RO
# vac 1s
payload = HC1:NCFOXN%TSMAHN-HUSC7LDZL18ZT4 E1V8.9B7AJU-SXG4X75MLE:X9LGCG+RK1JZZPQA36S4HZ6SH9X5QN9IFY1OSMNV1L8VNF6AYMZUUGH18VH. 63:U$V6QAASH932Q-RTKK9+OC+G9QJPNF67J6QW6A$QRZM6PP3.5Y0Q$UPR$5:NLOEPNRAE69K P3KP*PP:+P*.1D9R+Q6646-$0AX67PPDFPVX1R270:6NEQ0R6AOMUF5LDCPF5RBQ746B46O1N646RM9AL5CBVW566LH 469/9-3AKI6-$MSR0J9C$ZJ*DJWP42W5SKRK:7R95H/5:P4A:7L7OCA7G6M8ORU9SSA7G6MGZ5V1R5.OU65FT5D75W9AV88G64GHCGW5K/C/:7+PK$NH9QF8-7+/H::21UU4NU/*OBU4.XGV8OO95A2QS7ROSMT*IF/PE9O 3VB%GIVIA8R*XJVNVW.155UY9LY+1R/73H0Y/8WIE
# vac 2s
payload = HC1:NCFOXN%TSMAHN-HUSC7LDZL18ZT4 E/R8E:INDCCH184DCJ91YE0PPP-I.BDAZAF/8X*G3M9CXP3+AZW4%+A63HNNVR*G0C7PHBO33:X0 MBSQJ%F3KD3CU84Z0QPFSZ4NM0%*47%S%*48YIZ73423ZQTX63-E32R4UZ2 NVV5TN%2UP20J5/5LEBFD-48YI+T4D-4HRVUMNMD3323R1370RC-4A+2XEN QT QTHC31M3+E3CP456L X4CZKHKB-43.E3KD3OAJ5%IWZKRA38M7323 PCQP9-JNLBJ09BYY88EK:M2VW5Q41W63OH3TOOHJP7NVDEB$/IL0J99SSZ4RZ4E%5MK96R96+PEN9C9Q9J1:.PNJPWH9 UPYF9Q/UIN9P8QOA9DIEF7F:-1G%5TW5A 6YO67N6D9ESJD2BFHXURIUC%55VTE:4IG9R6GCI69 52NF3TD%/2C4HABTDYVZGT%WMM4UG6M:5CNUR+54HVHAVLELA08MU1KMHFXLPVO4:7W3YB 20H3MW2
# rec
payload = HC1:NCFOXN%TSMAHN-HUSC7LDZL18ZT4 E8S8ELB7AJU-SXG4X75%LE:X9LGCG+RK1JZZPQA3DP4OW631AX5QN9IFY1OSMNV1L8VNF6AYMZUU7C1UF6-:U V6GK6FXA31A32Q-RTRH9/UPNF67J6QW6D90C KUGAACQG40SM92OGIC3LD32R4UZ2 NVV5TN%2UP20J5/5LEBFD-48YI5S4CZKHKB-43.E3KD3OAJ5AL5:4A93NOJ4LTZABMD3E-4RZ4E%5MK91UP6-5 T5$V9C9QQK9HWP C59.P+95XW5I%5B/94O5$01RFUDTUNQUIN9P8Q0LPTB12:UX81QV1G 1G%5TW5A 6YO67N6RBE0BQRLFL-AGNGPCLPLM9O644V5:Q/5N5-PMXJLZIA:QH7DM18*9FPSGJ49ZQO$Z5/M5REJ3SBNKV/7N7020NJEE9:*U11U%ROQBOKS0P%PEFE
# test
payload = HC1:NCFOXN%TSMAHN-HUSC7LDZL18ZT4 E/R8.C1NDCCH184D.H9+/SF%G4G5BEBN9HNO4*J8OX4SX42VLWLICN53O8J.V J8$XJK*L5R17PGA*LLWOA*F8XF3+PVE0D 9:PIQGG4SIWLHWVHWVH+ZE/T9NX1XF8/+H2T9.GGOUKOH6NSHOP6OH6XO9IE5IVU5P2-GA*PEVH6/IEKMAC+HAW1FNH%A2 S9BQN* 9-V9%OKAJ92J1QJAZM93$UWW2QRA H99QHOQ1TK96L6SR9MU9DV5 R1AMI8LHU-H/O1:O1AT1NQ1SH99H6-F0+V9.T9D 9PRAAUICO10W59UE1YHU-H:PI/E2$4JY/KUYCG+S:1JD-4M%I /K .K47TC4T+*431T:SCZIVI1HNK7L$G55LY0UD1VF1VHS9UM97H98$QJEQ8BH2GQHLK0QFNANDDD*HHL/FH%R:Z8- 5%JLEQ3DXU:$8C HWJM029B2WO3A0-PN/R9VNS+GS0O8U52WHI5HI3RBBI/XVH1LQGTR$J+2CX405XQ11
# BG
# emo_rec
payload = HC1:NCFOXN*TS0BI$ZDYSH$PJ6RQPM3 RF:D4YIJ-36HD7-TMLV4RJM5DODW24K6VEGNO4*J8OX4UZ85XPWLI3K5YO9OUUMK9WLIK*L5R1G$JA-LC%R/.N8WKTOOZTG3UB3-JJ*FOUK:PIWEGLS4AZKZ73423IFT4I3KD3O05%YITAFCNNM3L .GSC9EY8YA7PZBMXPP+PHI4W*PP+P8OI.I9Y*VSV0I+QWZJ4ZH0QIRR97I2HOAXL92L0G+SB.V Q5AO91DKUM4FIGIGF5JNBPI.QUH%5/1O43VYYNJK1G%UJ44EIA6LFJ$GDAIC:00.JE9E.A47LJF+A*/2V.46AL**I-FNHRV8KN5QN9Y4KCT9-S.TV1WVMP0GVV WVOOV%X47*KB*KYQTKWT4S8M.SU:B5LIDJIR9V.HTJ-ELRF25NS3NHVP7W0N5U$V3UHL0D48.ESFITV9QZB33JR/RCKF+OALQVR9QR*D9A7N3L%XF:*VGUS/IAFCDW3JV.G
# edi_vac 
payload = HC1:NCFOXN*TS0BI$ZDYSH$PJ6RQPM3 RF:D4$W2-36HD7-TM4X4936*CMLV4HN79LOQHIZC4:QM3OK9FH19SJUPY0BZW46+A$/IX:S:+IZW4PHBO33HD7AOB*$G/IB597YENSPB*QJEFFS8FYXVSZ4SL0.B9UKPSH9795E%6846A$Q 76SW6GO1:660F0N$KKQS7DS2*N.SSBNKA.G.P6A8IM%OVNI*$K3$OHBW24FAL86H0VOCIL8-TIK*R3T3+7A.N88J4R$F/MAITH6QS03L0QIRR97I2HOAXL92L0. K6MGK.5.REQ01K SP$I7ZK$M8JQEPZB8L4$M8TDN7LPMIH-O92UQXRUT*P386OQOUK1-162RND9W9+RC.U%%VANALV9P46Q60Q87+QOWI1CPIGSU9H6+W3UJ8YJ4O2WAXQAQ3R.2MRJ609UCQFRMLNKNM8JI0JPG+6H66MPU05E5$ZPM71D8N58KRKOOL87/IRK3.04+1SZRS3 PC0NK6S7$LR2DD U7:K.Z5AHK2AL-4QND5.B6P53UVUJ+CMANRYDW%SHB0WI510I
# IT
# vac
payload = HC1:6BFOXN%TS3DH0YOJ58S S-W5HDC *M0II5XHC9B5G2+$N IOP-IA%NFQGRJPC%OQHIZC4.OI1RM8ZA.A5:S9MKN4NN3F85QNCY0O%0VZ001HOC9JU0D0HT0HB2PL/IB*09B9LW4T*8+DCMH0LDK2%K:XFE70*LP$V25$0Q:J:4MO1P0%0L0HD+9E/HY+4J6TH48S%4K.GJ2PT3QY:GQ3TE2I+-CPHN6D7LLK*2HG%89UV-0LZ 2ZJJ524-LH/CJTK96L6SR9MU9DHGZ%P WUQRENS431T1XCNCF+47AY0-IFO0500TGPN8F5G.41Q2E4T8ALW.INSV$ 07UV5SR+BNQHNML7 /KD3TU 4V*CAT3ZGLQMI/XI%ZJNSBBXK2:UG%UJMI:TU+MMPZ5$/PMX19UE:-PSR3/$NU44CBE6DQ3D7B0FBOFX0DV2DGMB$YPF62I$60/F$Z2I6IFX21XNI-LM%3/DF/U6Z9FEOJVRLVW6K$UG+BKK57:1+D10%4K83F+1VWD1NE
# rec
payload = HC1:6BFOXN%TS3DH0YOJ58S S-W5HDC *MEB2B2JJ59J-9BC6:X9NECX0AKQC:3DCV4*XUA2P-FHT-H4SI/J9WVHWVH+ZEOV1J$HNTICZUBOM*LP$V25$0Q:J40IA3L/*84-5%:C92JN*4CY0*%9F/8J2P4.818T+:IX3M3.96RPVD9J-OZT1-NT0 2$$0$2PZX69B9VCDHI2/T9TU1BPIJKH/T7B-S-*O/Y41FD+X49+5Z-6%.HDD8R6W1FDJGJSFJ/4Q:T0.KJTNP8EFULNC:HA0K5HKRB4TD85LOLF92GF.3O.Z8CC7-2FQYG$%21 2O*4R60NM8JI0EUGP$I/XK$M8ZQE6YB9M66P8N31I.ROSK%IA1Q2N53Q-OQ2VC6E26T11ROSNK5W-*H+MJ%0RGZVGWNURI75RBSQSHLH1JG*CMH2.-S$7VX6N*Z1881J7G.F9I+SV06F+1M*93%D
# test
payload = HC1:6BFOXN%TS3DH0YOJ58S S-W5HDC *M0IIE 1C9B5G2+$NP-OP-IA%N%QHRJPC%OQHIZC4.OI:OIG/Q80P2W4VZ0K1H$$0CNN62PK.G +AG5T01HJCAMKNAB5S.8%*8Z95%9EMP8N22MM42WFCD9C2AKIJKIJM1MQIAY.D-7A4KE0PLV1ARKF.GH5$C4-9GGIUEC0QE1JAF.714NTPINRQ3.VR+P0$J2*N$*SB-G9+RT*QFNI2X02%KYZPQV6YP8412HOA-I0+M9GPEGPEMH0SJ4OM9*1B+M96K1HK2YJ2PI0P:65:41ZSW$P*CM-NT0 2$88L/II 05B9.Z8T*8Y1VM:KCY07LPMIH-O9XZQ4H9IZBP%D2U3+KGP2W2UQNG6-E6+WJTK1%J6/UI2YUELE+W35T7+H8NH8DRG+PG.UIZ$U%UF*QHOOENBU621TW5XW5HS9+I010H% 0R%0ZD5CC9T0HP8TCNNI:CQ:G172DX8FZV3U9W-HNPPQ N2KV 2VHDHO:2XAV:FB+18DRR%%VQ F60LF6K 38GK8LGG4U7UP6*S4QBR-F97FRONPKZS+P9$5W1CAV37KD48ERCRH
"""
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
# Debugging in case of new json struct
print("Debugging...")
print("__________________________")
print(whole)
print("Date from: " + str(datetime.fromtimestamp(j_whole['6']).date()))
print("Date until: " + str(datetime.fromtimestamp(j_whole['4']).date()))
print("__________________________")
print(" ")
os.system("pause")
"""


# Checking validity
def validity():
    today = datetime.today().date()  # getting today's date
    # Forming the date to check by adding the days from the .ini file to the date from the cert
    if var == 1:
        Date = datetime.fromtimestamp(j_whole['4']).date()
    elif var != 1:
        Date = date_from + relativedelta(months=vall)
    # Comparing the date of expire against today
    if today < Date:  # Valid cert
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
    print(" ")
    print(".:::::::::::::::::::::::::::::::::::::::Recovery certificate::::::::::::::::::::::::::::::::::::::::.")
    print("Certificate information: ")
    print("Native Name: " + str(j_whole['-260']['1']['nam']['gn'])  + " " + str(j_whole['-260']['1']['nam']['fn']))
    print("EN Name: "     + str(j_whole['-260']['1']['nam']['gnt']) + " " + str(j_whole['-260']['1']['nam']['fnt']))
    print("Valid from:  " + str(datetime.fromtimestamp(j_whole['6']).date()))
    print("Valid until: " + str(datetime.fromtimestamp(j_whole['4']).date()))
    print("Unique Certificate Identifier: " + str(j_whole['-260']['1']['r'][0]['ci']))
    for K, V in CO.items():
        if j_whole['1'] == K:
            print("Country: " + V)
        elif len(j_whole['1']) > 2:
            print("Country: " + (j_whole['1']))
    validity()

# Vaccine cert
def vac_cert():
    os.system("cls")
    print(".:::::::::::::::::::::::::::::::::::EU DIGITAL COVID CERTIFICATE::::::::::::::::::::::::::::::::::::.")
    print(".:::::::::::::::::::::::::::::::::::ЦИФРОВ COVID СЕРТИФИКАТ НА ЕС:::::::::::::::::::::::::::::::::::.")
    print(" ")
    print(".::::::::::::::::::::::::::::::::::::::Vaccination certificate::::::::::::::::::::::::::::::::::::::.")
    print("Certificate information: ")
    print("Native Name: " + str(j_whole['-260']['1']['nam']['gn'])  + " " + str(j_whole['-260']['1']['nam']['fn']))
    print("EN Name: "     + str(j_whole['-260']['1']['nam']['gnt']) + " " + str(j_whole['-260']['1']['nam']['fnt']))
    print("Date Issued: " + str(datetime.fromtimestamp(j_whole['6']).date()))
    print("Valid until: " + str(datetime.fromtimestamp(j_whole['4']).date()))
    print("Unique Certificate Identifier: " + j_whole['-260']['1']['v'][0]['ci'])
    for K, V in CO.items():
        if j_whole['1'] == K:
            print("Country: " + V)
        elif len(j_whole['1']) > 2:
            print("Country: " + (j_whole['1']))
    validity()

# Test cert
def test_cert():
    os.system("cls")
    print(".:::::::::::::::::::::::::::::::::::EU DIGITAL COVID CERTIFICATE::::::::::::::::::::::::::::::::::::.")
    print(".:::::::::::::::::::::::::::::::::::ЦИФРОВ COVID СЕРТИФИКАТ НА ЕС:::::::::::::::::::::::::::::::::::.")
    print(" ")
    print(".:::::::::::::::::::::::::::::::::::::::::Test certificate::::::::::::::::::::::::::::::::::::::::::.")
    print("Certificate information: ")
    print("Native Name: " + str(j_whole['-260']['1']['nam']['gn'])  + " " + str(j_whole['-260']['1']['nam']['fn']))
    print("EN Name: "     + str(j_whole['-260']['1']['nam']['gnt']) + " " + str(j_whole['-260']['1']['nam']['fnt']))
    print("Date Issued: " + str(datetime.fromtimestamp(j_whole['6']).date()))
    print("Valid until: " + str(datetime.fromtimestamp(j_whole['4']).date()))
    print("Unique Certificate Identifier: " + j_whole['-260']['1']['t'][0]['ci'])
    for K, V in CO.items():
        if j_whole['1'] == K:
            print("Country: " + V)
        elif len(j_whole['1']) > 2:
            print("Country: " + (j_whole['1']))
    validity()

# Determining the kind of cert. Error handling in case it fails to parse it correctly. Taking the validity period from
# the corresponding .ini file
dick = j_whole['-260']['1']                              # the dic with the needed information for the funcs above
date_from = datetime.fromtimestamp(j_whole['6']).date()  # date issued/valid from
var = "something"                                        # just a way to diff test cert
for k, v in dick.items():
    if k == "r":       # recovery
        if v is None:  # if empty will continue to the next sub-dic
            continue
        # Building variables
        if j_whole['1'] == "BG":  # In BG this cert is 365 days, not 180... for now
            val = open("val_rec_bg.ini", "r")  # Opens it in read mode
            vall = list(val)                # Converting data to list
            vall = int(vall[0])             # Taking the first (and only) item and convert it to int
            val.close()                     # Closes the file
        elif j_whole['1'] != "BG":
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
        val = open("val_vac.ini", "r")
        vall = list(val)
        vall = int(vall[0])
        val.close()
        try:
            vac_cert()
        except:
            exception()
            reset()
    elif k == "t":  # test cert
        if v is None:
            continue
        var = 1
        test_cert()
        try:
            test_cert()
        except:
            exception()
            reset()
#    else:
#        print("New or unsupported format. Please contact development team.")
#        os.system("pause")



# Old blocks for backup
"""
# Checking validity
def validity():
    today = datetime.today()
    # Forming the date to check by adding the days from the .ini file to the date from the cert
    if len(date_from) == 10:
            date = datetime.strptime(date_from, '%Y-%m-%d') + timedelta(days=vall)
    elif len(date_from) > 10:
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
    print("Native Name: " + str(j_whole['-260']['1']['nam']['gn'])  + " " + str(j_whole['-260']['1']['nam']['fn']))
    print("EN Name: "     + str(j_whole['-260']['1']['nam']['gnt']) + " " + str(j_whole['-260']['1']['nam']['fnt']))
    print("Valid from:  " + str(j_whole['-260']['1']['r'][0]['df']))
    print("Valid until: " + str(j_whole['-260']['1']['r'][0]['du']))
    print("Unique Certificate Identifier: " + str(j_whole['-260']['1']['r'][0]['ci']))
    for K, V in CO.items():
        if j_whole['1'] == K:
            print("Country: " + V)
        elif len(j_whole['1']) > 2:
            print("Country: " + (j_whole['1']))
    validity()

# Vaccine cert
def vac_cert():
    os.system("cls")
    print(".:::::::::::::::::::::::::::::::::::EU DIGITAL COVID CERTIFICATE::::::::::::::::::::::::::::::::::::.")
    print(".:::::::::::::::::::::::::::::::::::ЦИФРОВ COVID СЕРТИФИКАТ НА ЕС:::::::::::::::::::::::::::::::::::.")
    print(" ")
    print(".::::::::::::::::::::::::::::::::::::::Vaccination certificate::::::::::::::::::::::::::::::::::::::.")
    print("Certificate information: ")
    print("Native Name: " + str(j_whole['-260']['1']['nam']['gn'])  + " " + str(j_whole['-260']['1']['nam']['fn']))
    print("EN Name: "     + str(j_whole['-260']['1']['nam']['gnt']) + " " + str(j_whole['-260']['1']['nam']['fnt']))
    print("Date Issued: " + str(date_from))
    if len(date_from) == 10:
            date = datetime.strptime(date_from, '%Y-%m-%d') + timedelta(days=vall)
    elif len(date_from) > 10:
            date = datetime.strptime(date_from[:10], '%Y-%m-%d') + timedelta(days=vall)
    print("Valid until: " + str(date))
    print("Unique Certificate Identifier: " + j_whole['-260']['1']['v'][0]['ci'])
    for K, V in CO.items():
        if j_whole['1'] == K:
            print("Country: " + V)
        elif len(j_whole['1']) > 2:
            print("Country: " + (j_whole['1']))
    validity()

# Test cert
def test_cert():
    os.system("cls")
    print(".:::::::::::::::::::::::::::::::::::EU DIGITAL COVID CERTIFICATE::::::::::::::::::::::::::::::::::::.")
    print(".:::::::::::::::::::::::::::::::::::ЦИФРОВ COVID СЕРТИФИКАТ НА ЕС:::::::::::::::::::::::::::::::::::.")
    print(" ")
    print(".:::::::::::::::::::::::::::::::::::::::::Test certificate::::::::::::::::::::::::::::::::::::::::::.")
    print("Certificate information: ")
    print("Native Name: " + str(j_whole['-260']['1']['nam']['gn'])  + " " + str(j_whole['-260']['1']['nam']['fn']))
    print("EN Name: "     + str(j_whole['-260']['1']['nam']['gnt']) + " " + str(j_whole['-260']['1']['nam']['fnt']))
    print("Date Issued: " + str(j_whole['-260']['1']['t'][0]['sc']))
    if len(date_from) == 10:
            date = datetime.strptime(date_from, '%Y-%m-%d') + timedelta(days=vall)
    elif len(date_from) > 10:
            date = datetime.strptime(date_from[:10], '%Y-%m-%d') + timedelta(days=vall)
    print("Valid until: " + str(date))
    print("Unique Certificate Identifier: " + j_whole['-260']['1']['t'][0]['ci'])
    for K, V in CO.items():
        if j_whole['1'] == K:
            print("Country: " + V)
        elif len(j_whole['1']) > 2:
            print("Country: " + (j_whole['1']))
    validity()


# Determining the kind of cert. Error handling in case it fails to parse it correctly. Taking the validity period from
# the corresponding .ini file
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
        if j_whole['1'] == "BG":  # In BG this cert is 365 days, not 180
            vall = vall + 185
        try:
            sick_cert()  # calling the right func
        except:
            exception()
            reset()
    elif k == "v":  # vaccine
        if v is None:
            continue
        if len(j_whole['-260']['1']['v']) > 1:  # for two shots vac cert
            date_from = j_whole['-260']['1']['v'][1]['dt']
        else:
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