from libs.mojstd.py import *
from libs.bootCheck import *
import os

BootCheck() # Return True, so in case of plugin to start at boot it boot it 
execPlugins() 
  
returner()
os.system("sudo python menu.py")