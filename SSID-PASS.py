import subprocess

def save_wifi_passwords():
    try:
        result = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8', errors="backslashreplace").split('\n')
        profiles = [i.split(":")[1][1:-1] for i in result if "All User Profile" in i]
        
        with open("wifi_passwords.txt", "w", encoding="utf-8") as file:
            for profile in profiles:
                try:
                    password_result = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', 'name=' + profile, 'key=clear']).decode('utf-8', errors="backslashreplace").split('\n')
                    password = [b.split(":")[1][1:-1] for b in password_result if "Key Content" in b]
                    if password:
                        file.write(f"SSID     : {profile}\n")
                        file.write(f"Password : {password[0]}\n")
                        file.write("------------------------\n")
                    else:
                        file.write(f"SSID : {profile}\n")
                        file.write("Password for this user not found!\n")
                        file.write("------------------------\n")
                except subprocess.CalledProcessError:
                    file.write(f"Error to get Password for: SSID {profile}\n")
                    file.write("------------------------\n")

    except subprocess.CalledProcessError:
        print("Error to show the profiles list!")

save_wifi_passwords()