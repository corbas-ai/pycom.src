import struct
import time
import zlib
import logging
import binascii

log = logging.getLogger('crc')

def crc16_1(data):
    crc = 0x0000;
    for b in data:
        crc ^= (0xffff&b) << 8
        i = 0
        while(i<8):
            crc = (crc<<1)^0x8005 if crc&0x8000 else crc<<1
            i+=1
    return crc&0xffff

def pcrc16(data):
    """ calc crc16 and put it at tail  [-2:]. """
    crc = crc16_1(data[:-2])
    struct.pack_into(">H",data,len(data)-2,crc)

def check_crc16_1(data):
    datalen = len(data)-2
    crc, = struct.unpack_from(">H",data,offset=datalen)
    ncrc = crc16_1(data[:datalen])
    #log.debug("pack crc {} vs ncrc {}".format(ncrc,crc))
    return crc == ncrc


if __name__ == '__main__':
    l = 18
    data = bytearray(l)

    t = time.time()
    for i in range(l-4):
        data[i]=0xff
        pcrc16(data)
        if not check_crc16_1(data):
            print('WRONG crc on step {}'.format(i))
    print("pack iters={} crc16 at {:0.6f} per ones  final pack {} final crc {:04X}".format(l-4,(time.time()-t)/(l-4), binascii.hexlify(data),crc16_1(data[:l-2])))
    pcrc16(bytearray(2))
    data = bytearray(l)
    t=time.time()
    for i in range(l-4):
        data[i]=0xff
        crc = zlib.crc32(data[:-4]) & 0xffffffff
        struct.pack_into(">I",data,l-4,crc)
        packcrc, = struct.unpack_from(">I",data,len(data)-4)
        checkcrc = zlib.crc32(data[:-4]) & 0xffffffff
        if packcrc!=checkcrc:
            print('WRONG crc32 on step {}'.format(i))

    print("crtc crc32 at {:>0.5f} per ones".format((time.time()-t)/(l-4)))

    td  = bytearray([b for b in range(256)])

    print("crc16_1: {:04X}h  and crc32: {:08X}h".format(crc16_1(td)&0xffffffff,zlib.crc32(td,0x0)))
