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
    saved_ssids = []

    for line in enum:
        if 'All User Profile' in line:
            ssid = line.split(':')[1].strip()
            saved_ssids.append(ssid)
    # Make a list of passwords
    passwords_list = []
    for wifi_ssid in saved_ssids:
        query = 'netsh wlan show profiles name=%s key=clear' % (wifi_ssid)
        output = subprocess.check_output(query)
        if 'Key Content' in str(output):
            output = str(output) .split("\\r\\n")
            for line in output:
                if 'Key Content' in line:
                    password = line.split(':')[1].strip()
                    passwords_list.append(password)
                    # print("Password for SSID %s is %s" % (wifi_ssid, password))
        else:
            passwords_list.append("\033[31mNOT FOUND \033[m")  # Change text color to red

elif 'linux' in sys.platform:   # Linux platform
    os.chdir('/etc/NetworkManager/system-connections/')  # Move to folder
    saved_ssids = os.listdir()  # List of saved SSIDs
    # Make a list of passwords
    passwords_list = []
    for item in saved_ssids:
        with open(item) as file:
            if 'psk' in file.read():
                content = file.readlines()
                for item in content:
                    if 'psk' in item:
                        password = item.split('=')[1]
                        passwords_list.append(password)
                    # print("Password for SSID %s is %s" % (wifi_ssid, password))
            else:
                passwords_list.append("\033[31mNOT FOUND \033[m")  # Change text color to red

# Present the result:
wifi_pw = dict(zip(saved_ssids, passwords_list))
print('SSID'.ljust(15), '|'.ljust(1), 'Password')
print('-'*30)
for item in wifi_pw.items():
    print(item[0].ljust(15), '|'.ljust(1), item[1])
