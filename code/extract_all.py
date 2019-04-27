import os
import subprocess
import sys
'''
This script will extract all saved wifi passwords on a computer.
'''
if 'win' in sys.platform:  # Windows platform
    enum = 'netsh wlan show profiles'
    enum = subprocess.check_output(enum)
    enum = str(enum).split("\\r\\n")
    # Make a list of saved SSIDs
    profile_list = []
    for line in enum:
        if 'All User Profile' in line:
            ssid = line.split(':')[1].strip()
            profile_list.append(ssid)
    # Extract the passwords
    for wifi_ssid in profile_list:
        query = 'netsh wlan show profiles name=%s key=clear' % (wifi_ssid)
        output = subprocess.check_output(query)
        output = str(output) .split("\\r\\n")
        for line in output:
            if 'Key Content' in line:
                password = line.split(':')[1].strip()
                print("Password for SSID %s is %s" % (wifi_ssid, password))
elif 'linux' in sys.platform:   # Linux platform
    os.chdir('/etc/NetworkManager/system-connections/')  # Move to folder
    saved_ssids = os.listdir()  # List of saved SSIDs
    for item in saved_ssids:
        with open(item) as file:
            content = file.readlines()
            for item in content:
                if 'psk' in item:
                    password = item.split('=')[1]
                print("Password for SSID %s is %s" % (wifi_ssid, password))
