import machine
from network import WLAN
import pycom
import utime as time
import ustruct as struct

import usocket as socket
import uselect as select
from ubinascii import hexlify as tohex

pycom.heartbeat(0)

sleep = time.sleep
fmt = '<IbI'
PERIOD=.5


def main():
    pycom.rgbled(0x010201)
    wlan = WLAN() # get current object, without changing the mode
    if machine.reset_cause() != machine.SOFT_RESET:
        wlan.init(mode=WLAN.STA)
        # configuration below MUST match your home router settings!!
        wlan.ifconfig(config=('192.168.58.124', '255.255.255.0', '192.168.58.1', '8.8.8.8')) # (ip, subnet_mask, gateway, DNS_server)
    reconnect()
    task()

def reconnect():
    wlan = WLAN()
    while not wlan.isconnected():
        # change the line below to match your network ssid, security and password
        wlan.connect('br232', auth=(WLAN.WPA2, 'sahbeeyi'), timeout=5000)
        print("connecting",end='')
        try:
            while not wlan.isconnected():
                pycom.rgbled(0x030104)
                time.sleep(.5)
                pycom.rgbled(0x040101)
                time.sleep(.5)
                print(".",end='')
                
            print("connected")
            pycom.rgbled(0x010301)
        except :
            time.sleep(1)
        
        

def task():
    LEN = 64
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    pack = bytearray([i for i in range(LEN)])
    ack = bytearray(LEN)
    gett = time.ticks_ms
    poll = select.poll()
    latency = 100
    period = PERIOD
    target = ('192.168.1.22',5760)
    tic = 0
    r = 0
    while True:
        try:
            pycom.rgbled(0x010103) #white
            struct.pack_into(fmt,pack,0,tic,ord('c'),0)
            print('ping %s to %s pack(%d):%s '%(tic,target,len(pack),tohex(pack)))
            sock.sendto(pack,target)
            st = gett()
            poll.register(sock,select.POLLIN)
            evt = poll.poll(latency)
            if evt:
                r = 0
                
                for ev in evt:
                    fd = ev[0]
                    
                    if fd == sock or fd == sock.fileno():
                        print("<1>",ev, sock)
                        ack,addr = sock.recvfrom(LEN)
                        et = gett()
                        ttic, c , sensor = struct.unpack_from(fmt,ack,0)
                        pycom.rgbled(0x000400) #green
                        print("%d...recv ttic:%d, tag:%s, sensor:%d from %s pack(%s):%s at %.05f"%(tic, ttic, c, sensor, addr, r,tohex(ack[:r]),et-st))
            else:
                print("%d.....recv nothing." % tic)
                pycom.rgbled(0x030000) #red
            sleep(period)
            tic += 1
        except OSError:
            reconnect()

if __name__ == '__main__':
    main()