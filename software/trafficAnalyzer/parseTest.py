import socket
import struct

soc=socket.socket(socket.AF_INET6,socket.SOCK_DGRAM)
soc.bind(('',16792))
b=bytearray(56)
while True:
    size,addr=soc.recvfrom_into(b,56)
    result=struct.unpack('<'+'BHHbB'*8,str(b))
    #result = struct.unpack('<'+'b'*56,str(b))
    for index in range(0,40,5):
        channel=result[index]
        tx=result[index+1]
        ack=result[index+2]
        rssi=result[index+3]
        lqi=result[index+4]
        print addr[0].split(':')[-1],'C:'+str(channel),str(ack)+'/'+str(tx),'RSSI='+str(rssi),'LQI='+str(lqi)
