#에코서버

from socket import * 

HOST = 'localhost'
PORT = 81

s = socket(AF_INET,SOCK_DGRAM) #소캣 32bit UDP
s.bind((HOST,PORT))

while True:
    data,addr = s.recvfrom(1024)
    print('ip :',addr[0], "\tport:",addr[1])
    print('Data :', data.decode())
    s.sendto(data,addr)
