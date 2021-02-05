"""Тест скорости по сравнению с Arduino"""

Arduino_sketch="""

/**
 *  It takes 703 micros on Arduino DUE
 */

#include <stdint.h>

typedef uint16_t t_group;
#define N_GROUPS  200
t_group arr[N_GROUPS];

void setup() {
  Serial.begin(9600);
  for (int i = 0 ; i < sizeof(arr) / sizeof(arr[0]); i++) {
    arr[i] = 0x01a8;
  }
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  static int cntr = 0;
  Serial.print(cntr);
  Serial.print(". ");
  digitalWrite(LED_BUILTIN, HIGH);
  test_1();
  digitalWrite(LED_BUILTIN, LOW);
  delay(500);
  ++cntr;
}

void test_1() {
  Serial.print("Test 1 ");
  unsigned int st = micros();
  unsigned int crc = 0;
  for (int i = 0; i < 10; i++) {
    crc = crc16_f(arr, sizeof(arr));
  }
  unsigned et = micros();
  Serial.print(" crc16_f: ");
  Serial.print(crc, HEX);
  Serial.print('h');
  Serial.print(" takes ");
  Serial.print(et - st);
  Serial.println(" microseconds");
}

unsigned short crc16_f(void* buffer, int size){
  if( size <= 0 ){
    return 0;
  }
  unsigned char * buff = (unsigned char *)buffer;
  unsigned short crc = 0;
  while (size--){
    crc ^= *buff++ << 8;
    for (int i = 0; i < 8; i++)
      crc = crc & 0x8000 ? ( crc << 1 ) ^ 0x8005 : crc << 1 ;
  }
  return crc;
}
"""

import time
#micros = time.ticks_us
millis = time.ticks_ms
#nanos = time.monotonic_ns

def crc16_1(data):
    crc = 0x0000;
    for b in data:
        crc ^= (0xffff&b) << 8
        i = 0
        while(i<8):
            crc = (crc<<1)^0x8005 if crc&0x8000 else crc<<1
            i+=1
    return crc&0xffff

def main():
    N_GROUPS = 200
    BPG = 2
    arr = bytearray(BPG*N_GROUPS)
    for i in range(N_GROUPS):
        arr[i*BPG] = 0xa8; arr[i*BPG+1] = 0x01
    cntr = 0
    while True:
        st = millis()
        crc = 0
        for i in range(10):
            crc = crc16_1(arr)
        et = millis()
        print("{}. crc16_f: {:04x}h takes {} millis)".format(cntr,crc,et-st))
        time.sleep(.500)
        cntr += 1
