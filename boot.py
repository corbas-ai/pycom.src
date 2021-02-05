# boot.py -- run on boot-up
from network import WLAN
import pycom

wlan = WLAN(mode=WLAN.STA)
pycom.heartbeat(0)