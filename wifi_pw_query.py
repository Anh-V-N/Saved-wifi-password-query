# import os
import subprocess
import sys

# print(sys.platform)
print('Query the password for a saved SSID')
wifi_ssid = input("Specify the SSID: ")

if 'win' in sys.platform:
    query = 'netsh wlan show profiles name=%s key=clear' % (wifi_ssid)
    try:
        output = subprocess.check_output(query)
        output = str(output) .split("\\r\\n")
        # print(len(output))
        # print(output)
        for line in output:
            if 'Key Content' in line:
                line = line.split(':')
                print("Password for %s is %s" % (wifi_ssid, line[1]))
    except Exception as err:
        print(err)
        print('SSID %s is not found in the system' % (wifi_ssid))
