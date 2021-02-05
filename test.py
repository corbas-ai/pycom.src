import pycom
import time

pycom.heartbeat(0)
for cycles in range(10):
    pycom.rgbled(0x007f00) #green
    time.sleep(5)
    pycom.rgbled(0x7f7f00) #yellow
    time.sleep(1.5)
    pycom.rgbled(0x7f0000) # red
    time.sleep(4)
