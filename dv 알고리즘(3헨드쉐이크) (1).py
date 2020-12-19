#-*- coding: utf-8 -*-
#!/usr/bin/env python

#시간 측정
import time
#바이너리 변환
from struct import *
from socket import *
import socketserver
import sys 
import select

HOST = 'localhost'
PORT = 81
BUFSIZE = 1024


class GrammerError(Exception):
    pass
class BaseNet:
    SYN = False
    ACK = False
    client = None
    
    def __init__(s,host='localhost',port=81,server=True):
        s._socket = socket(AF_INET,SOCK_DGRAM) #소캣 32bit UDP
        s.server = server
        s.HOST = (host,port)#서버 타겟 지정
        if server :
            #서버측이라면
            s._socket.bind((s.HOST))#오픈
            s.client = []
        else :
            #클라이언트 처리
            s._socket.bind(('',0))#오픈
            s.client = s._socket.laddr #자신의 ip와  포트 번호
            s.SYN = True # 헨드쉐이크 온
            s._socket.sendto(s.makeheader())#헤더 전송하여 헨드쉐이크
        s.seq = 0
        s.ack = 0
        #h,p = s.laddr
        #s.HOST = (server and '' or host,server and port or p) #포트 수정하여 기입

    '''
    16 / 16     //발신지 / 수신지 포트
    32          //시퀸스 넘
    32          //에크넘버
    4 / 6 / 6/ 16 //해더길이 필드/예약/플래그 비트 / 윈도 크기
    16 / 16     //체크섬/ 
    
    '''

    def makeheader(s,addr=None):
        out = None

        if s.server:
            h,p = s.HOST
            out = pack('i',p)#발신지
            h,p = addr
            out+= pack('i',p)#수신지
        else :
            h,p = s.client
            out = pack('i',p)#발신지
            h,p = s.HOST
            out+= pack('i',p)#수신지
            
        #out = pack('i',p) + pack('i',port)#발신지/ 수신지 (처음은 알 수 없기에 걍 전송)
        out += pack('dd',0,0)#ack 와 seq 는 안씀 (데이터 X)
        out += pack('xxxxxxxx')#10비트를 무시(0으로 채움) data offset / + 4
        out += pack('d',s.__getFlag())#2bit / URG / ACK / PSH / PST / SYN / FIN   1/2/(4)/(8)/16/(32)/(64)/(128)
        out += pack('dd',0,0)#윈도 사이즈
        return out

    def getheader(s,data):
        (p1,p2,s.seq,s.ack,flag,i,i) = unpack('iiddxxxxxxxxddd',data)
        s.__setFlag(s,flag)
        print((p1,p2,s.seq,s.ack,flag,i,i))
        
    def __getFlag(s,fin = False):
        out = fin and 1 or 0
        out+= s.SYN and 2 or 0
        out+= s.ACK and 16 or 0
        return out
    
    def __setFlag(s,f):
        out  = [i == '1' for i in format(f,'b')]
        s.ACK = out[0]
        s.SYN = out[3]
        return out[4]
        
        
    #syn / seq / ack
    def handSakeHeader(s,data):
        #pack('b',)#0~255
        if data:
            syn = d
        if s.server:
            #서버일 경우
            if not data:
                raise GrammerError("문법에러 : 헨드쉐이크")
            s.syn = True
            #seq
            #s.ack
        else:
            if s.ack:#ack가 전송되어 왔을경우
                s.syn = False
            #클라이언트 일 경우
            s.syn = True
            #s.seq = 
            s.ack = 0


        return pack('?',s.syn) + pack('B',s.seq) + pack('B',s.ack)
#=========================================================================
#Server
class Server(BaseNet):

    def __init__(s,port = 81,server=True):
        super().__init__(port)
        print(super().makeheader())#헨드쉐이킹 전송

        print(super()._socket.recvfrom(20))
    
#=========================================================================
#Client
class Client(BaseNet):

    def __init__(s,host = 'localhost',port = 81):
        super().__init__(port)
        super().makeheader()#헨드쉐이킹 전송

        s.recv()
    def recv(s):
        data = s._socket.recvfrom(20)
        print(data)
        super().getheader(data)
    
    def sendto(s):
        pass
    
    
def client():
    '''
    f=open (filename, "rb") #파일 일기용으로 열기
    data = f.read(BUFSIZE) #파일 읽기
    while (data): 
        if(s.sendto(data,addr)): #파일 내용 전송
         print ("uploading ...") 
         data = f.read(BUFSIZE) 
    f.close()
    '''
    s.close()

#=========================================================================
def usage():
    sys.stdout = sys.stderr
    print ('Usage: python FileUDP.py -s [port]            (server)')
    print ('or:    python FileUDP.py -c host [port] <file (client)')
    # 종료
    sys.exit(2)


def __main__():

    if len(sys.argv) < 2:
        usage()
    
    if sys.argv[1] == '-s':
        #서버 함수 호출 
        Server()
    # 첫 매개변수가 '-c' 라면
    elif sys.argv[1] == '-c':
        #클라이언트 함수 호출
        Client()
__main__()
