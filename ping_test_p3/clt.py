import socket
import select
import struct
import time
import sys
import os
import binascii

tohex = binascii.hexlify

LEN=64
recv_pack = bytearray(LEN)
gett = time.time
sleep = time.sleep
fmt = '<IcI'
PERIOD=.5


def run(target, latency, period=1.):
    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sock.setblocking(0)
    pack = bytearray([i for i in range(LEN)])
    ack = bytearray(LEN)
    poll = select.poll()
    tic = 0
    r = 0
    while True:
        struct.pack_into(fmt,pack,0,tic,b'c',0)
        print('ping %s to %s pack(%d):%s '%(tic,target,len(pack),tohex(pack)))
        sock.sendto(pack,target)
        st = gett()
        poll.register(sock,select.POLLIN)
        evt = poll.poll(latency*1e3)
        if evt:
            r = 0
            for ev in evt:
                fd = ev[0]
                if fd == sock.fileno():
                    r,addr = sock.recvfrom_into(ack)
                    et = gett()
                    ttic, c , sensor = struct.unpack_from(fmt,ack,0)
                    print("%d...recv ttic:%d, tag:%s, sensor:%d from %s pack(%s):%s at %.05f"%(tic, ttic, c, sensor, addr, r,tohex(ack[:r]),et-st))
        else:
            print("%d.....recv nothing." % tic)
        sleep(period)
        tic += 1


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("need target ip:port")
        os._exit(1)
    target = sys.argv[1]
    ip,port = target.split(":")
    port = int(port)
    print("%s:%d"%(ip,port))
    run((ip,port),latency=0.001, period=PERIOD)
