import subprocess
import re

def get_wifi_passwords():
    # 1. Get all wifi profiles
    command_output = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="backslashreplace")
    
    # Extract profile names using regex
    profile_names = re.findall(r"utente\s*:\s*(.*)\r", command_output)
    
    wifi_list = []
    
    if len(profile_names) != 0:
        for name in profile_names:
            wifi_profile = {}
            # 2. Get details for each profile
            profile_info = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', name, 'key=clear']).decode('utf-8', errors="backslashreplace")
            
            # Extract password (Key Content)
            password = re.search(r"Contenuto chiave\s*:\s*(.*)\r", profile_info)
            
            wifi_profile["ssid"] = name
            if password is None:
                wifi_profile["password"] = None
            else:
                wifi_profile["password"] = password[1]
                
            wifi_list.append(wifi_profile)
            
    return wifi_list

# Execute and print results
for wifi in get_wifi_passwords():
    print(f"SSID: {wifi['ssid']}, Password: {wifi['password']}")

input("Press Enter to exit...")
