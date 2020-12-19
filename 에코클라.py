#에코 클라

from socket import *

HOST = 'localhost'
PORT = 81

s = socket(AF_INET,SOCK_DGRAM) #소캣 32bit UDP
s.bind(('',0))

print(s)
get = input("전송할 데이터")
s.sendto(get.encode(),(HOST,PORT))
get = s.recvfrom(65535)

print(get)
