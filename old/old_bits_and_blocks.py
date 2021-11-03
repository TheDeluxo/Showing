#! /usr/bin/env python3

"""
# Visible input
print('Please, scan the QR\n')
print('Or type "exit" to quit\n')
payload = input() # waiting the user input
# if user type in "exit" will terminate the script and the window
if payload.lower() == "exit": # case insensitive
     sys.exit()
"""

# Recovery cert
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
    print("Country: " + (j_whole['1']))
    validity()

# Foreign recovery cert
def sick_foreign():
    os.system("cls")
    print(" .::::::::::::::::::::::::::::::::::::::EU DIGITAL COVID CERTIFICATE:::::::::::::::::::::::::::::::::::::::.")
    print(" .::::::::::::::::::::::::::::::::::::::ЦИФРОВ COVID СЕРТИФИКАТ НА ЕС::::::::::::::::::::::::::::::::::::::.")
    print("")
    print(" .::::::::::::::::::::::::::::::::::::::::::Recovery certificate:::::::::::::::::::::::::::::::::::::::::::.")
    print("Certificate information: ")
    print("Native Name: " + str(j_whole['-260']['1']['nam']['gn']) + " " + str(j_whole['-260']['1']['nam']['fn']))
    print("EN Name: "     + str(j_whole['-260']['1']['nam']['gnt']) + " " + str(j_whole['-260']['1']['nam']['fnt']))
    print("Valid from:  " + str(j_whole['-260']['1']['r'][0]['df']))
    print("Valid until: " + str(j_whole['-260']['1']['r'][0]['du']))
    print("Unique Certificate Identifier: " + str(j_whole['-260']['1']['r'][0]['ci'][9:]))
    print("Country: " + (j_whole['1']))
    validity()

# Vaccine cert
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
    print("Unique Certificate Identifier: " + j_whole['-260']['1']['v'][0]['ci'])
    print("Country: " + (j_whole['1']))
    validity()

# Foreign vacc cert
def vac_foreign():
    os.system("cls")
    print(" .::::::::::::::::::::::::::::::::::::::EU DIGITAL COVID CERTIFICATE:::::::::::::::::::::::::::::::::::::::.")
    print(" .::::::::::::::::::::::::::::::::::::::ЦИФРОВ COVID СЕРТИФИКАТ НА ЕС::::::::::::::::::::::::::::::::::::::.")
    print("")
    print(" .:::::::::::::::::::::::::::::::::::::::::Vaccination certificate:::::::::::::::::::::::::::::::::::::::::.")
    print("Certificate information: ")
    print("Native Name: " + str(j_whole['-260']['1']['nam']['gn'] + " "  + str(j_whole['-260']['1']['nam']['fn'])))
    print("EN Name: "     + str(j_whole['-260']['1']['nam']['gnt'] + " " + str(j_whole['-260']['1']['nam']['fnt'])))
    print("Date Issued: " + str(j_whole['-260']['1']['v'][0]['dt']))
    print("Unique Certificate Identifier: " + j_whole['-260']['1']['v'][0]['ci'])
    print("Country: " + (j_whole['1']))
    validity()

# Test cert
def test_cert():
    os.system("cls")
    print(" .::::::::::::::::::::::::::::::::::::::EU DIGITAL COVID CERTIFICATE:::::::::::::::::::::::::::::::::::::::.")
    print(" .::::::::::::::::::::::::::::::::::::::ЦИФРОВ COVID СЕРТИФИКАТ НА ЕС::::::::::::::::::::::::::::::::::::::.")
    print("")
    print(" .::::::::::::::::::::::::::::::::::::::::::::Test certificate:::::::::::::::::::::::::::::::::::::::::::::.")
    print("Certificate information: ")
    print("Native Name: " + str(j_whole['-260']['1']['nam']['gn']) + " " + str(j_whole['-260']['1']['nam']['fn']))
    print("EN Name: "     + str(j_whole['-260']['1']['nam']['gnt']) + " " + str(j_whole['-260']['1']['nam']['fnt']))
    print("Date Issued: " + str(j_whole['-260']['1']['t'][0]['sc']))
    print("Unique Certificate Identifier: " + j_whole['-260']['1']['t'][0]['ci'])
    print("Country: " + (j_whole['1']))
    validity()

# Determining the kind of cert
dick = j_whole['-260']['1']
for k, v in dick.items():
    if k == "r": # recovery
        if v is None:  # if empty will continue to the next sub-dic
            continue
        # building variables
        date_from = j_whole['-260']['1']['r'][0]['df']
        today = datetime.today()
        # calling the right func
        if j_whole['-260']['1']['r'][0]['co'] == "BG":
            sick()
        else:
            sick_foreign()
    elif k == "v": # vaccine
        if v is None:
            continue
        # building variables
        date_from = j_whole['-260']['1']['v'][0]['dt']
        today = datetime.today()
        # calling the right func
        if j_whole['-260']['1']['v'][0]['co'] == "BG":
            vac()
        else:
            vac_foreign()
    elif k == "t": # test cert
        if v is None:
            continue
        # building variables
        date_from = j_whole['-260']['1']['t'][0]['sc']
        today = datetime.today()
        # calling the right func
        test_cert()



"""
### OLD ###
# Determining the kind of cert
dick = j_whole['-260']['1']
for k, v in reversed(dick.items()):  # reverse walk through because of the "ver" position
    #print("current k = " + str(k) + " current v = " + str(v))  # dick walk result
    if k == "ver":  # saving the cert version
        ver = v
    if k == "r": # recovery
        #print("current k = " + str(k) + " current v = " + str(v))  # dick walk result
        if v == "null":
            continue
        # building variables
        date_from = j_whole['-260']['1']['r'][0]['df']
        today = datetime.today()
        # calling the right func
        if j_whole['-260']['1']['r'][0]['co'] == "BG":
            sick()
        else:
            sick_foreign()
    elif k == "v": # vaccine
        # building variables
        date_from = j_whole['-260']['1']['v'][0]['dt']
        today = datetime.today()
        # calling the right func
        if j_whole['-260']['1']['v'][0]['co'] == "BG":
            vac()
        else:
            vac_foreign()
    elif k == "t": # test cert
        # building variables
        date_from = j_whole['-260']['1']['t'][0]['sc']
        today = datetime.today()
        # calling the right func
        test_cert()
"""

