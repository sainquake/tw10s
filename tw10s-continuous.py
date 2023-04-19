from serial import Serial
import time

def modbusCrc(msg:bytearray) -> int:
    crc = 0xFFFF
    for n in range(len(msg)):
        crc ^= msg[n]
        for i in range(8):
            if crc & 1:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return crc

msg = [1,3,0]
msg.append(1)
msg.append(0)
msg.append(2)

crc = modbusCrc(bytearray(msg))
ba = crc.to_bytes(2, byteorder='little')
print("%02X %02X"%(ba[0], ba[1]))

msg.append(ba[0])
msg.append(ba[1])

print(msg)
print(str(bytearray(msg)))

ser = Serial('COM11', 9600, timeout=3)

ser.write(bytearray(msg))

t = time.time()

while(True):
    o = []
    o.append(ser.read())
    o.append(ser.read())
    o.append(ser.read())
    o.append(ser.read())

    if o == [b'\x01',b'\x03',b'\x04',b'\x00'] :
        #print('header ok',o)

        out = []
        for i in range(5):
            out.append(ser.read())

        #print(out)
        t2 = time.time()
        length = int.from_bytes(out[1], "big")*256 + int.from_bytes(out[2], "big")

        print('length=',length,'mm\t dt=',round((t2-t+0.00001)*1000),'us', flush=True)
    t = time.time()

