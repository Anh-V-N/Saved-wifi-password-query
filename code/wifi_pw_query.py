import os
import subprocess
import sys
'''
This script extracts the password fo a specificed saved SSID
'''
print('Query the password for a saved SSID')
wifi_ssid = input("Specify the SSID: ")

if 'win' in sys.platform:  # Windows platform
    query = 'netsh wlan show profiles name=%s key=clear' % (wifi_ssid)
    try:
        output = subprocess.check_output(query)
        output = str(output) .split("\\r\\n")  # Convert output to a list of strings
        for line in output:
            if 'Key Content' in line:
                password = line.split(':')[1].strip()
                print("Password for SSID %s is %s" % (wifi_ssid, password))
    except Exception as err:
        # print(err)
        print('SSID %s is not found in the system' % (wifi_ssid))

elif 'linux' in sys.platform:   # Linux platform
    os.chdir('/etc/NetworkManager/system-connections/')  # Move to folder
    saved_ssids = os.listdir()  # List of saved SSIDs
    file_exist = False
    for item in saved_ssids:
        if item.startswith(wifi_ssid):
            with open(item) as file:
                content = file.readlines()
                for item in content:
                    if 'psk' in item:
                        password = item.split('=')[1].strip()
                print("Password for SSID %s is %s" % (wifi_ssid, password))
                file_exist = True
    if file_exist is False:
        print('SSID %s is not found in the system' % (wifi_ssid))
