from libs.mojstd import *
from libs.bootCheck import *
from libs.updater import *
import os

def mon0():
        os.system("sudo iw wlan0 interface add mon0 type monitor")
        os.system("sudo airmon-ng start mon0")

if randomCheck():
    ui_print("Checking for\n   Updates...", 1)
    updateMain()
else: 
    pass


mon0()
BootCheck() # Return True, so in case of plugin to start at boot it boot it
# execPlugins()


os.system("sudo python menu.py")
