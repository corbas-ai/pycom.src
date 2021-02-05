import socket
import select
import struct
import sys
import binascii
import random

tohex = binascii.hexlify

inpack = bytearray(8000)
fmt = '<IcI'
def run(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('',port))
    sock.setblocking(0)
    print("bind on port %d"%port)
    poll = select.poll()
    poll.register(sock,select.POLLIN)
    sensor = 1
    prev = 0
    while True:
        evt = poll.poll()
        for ev in evt:
            fd = ev[0]
            if sock.fileno() == fd:
                r,addr = sock.recvfrom_into(inpack)
                tic,c,_ = struct.unpack_from(fmt,inpack,0)
                sensor = sensor + 1
                struct.pack_into(fmt, inpack, 0, tic, c, sensor ) 
                sock.sendto(inpack[:r],addr)
                print("ack(%d) to %s tic:%d, tag:%s, sensor:%d. pack:%s"%(r,addr,tic,c,sensor,tohex(inpack[:r])))

if __name__ == '__main__':
    port = 5760
    if len(sys.argv)>1:
        port = int(sys.argv[1])
    run(port)
