from network import WLAN
import machine
wlan = WLAN(mode=WLAN.STA)

nets = wlan.scan()
for net in nets:
    if net.ssid == 'br232':
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, 'sahbeeyi'), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        break
