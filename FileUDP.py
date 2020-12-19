#!/usr/bin/env python 

from socket import * 
import sys 
import select

HOST = 'localhost'
PORT = 81
BUFSIZE = 1024
#=========================================================================
#Server
def catchFileFromClient():
    s = socket(AF_INET,SOCK_DGRAM) #소캣 32bit UDP
    print(s.bind((HOST,PORT)) )
    print(s)

    f = open("out.txt",'wb') 
    data,addr = s.recvfrom(BUFSIZE) 

    while(data): 
        f.write(data) #데이터 작성
        s.settimeout(2) #패킷 타임아웃
        data,addr = s.recvfrom(BUFSIZE) #패킷 데이터 기다림
    #패킷의 끝을 알 수 없기 때문에 타임아웃 되기 기다림
    f.close()
    s.close()
 
def server():
    print('++++++파일 서버를 시작++++++')
    catchFileFromClient()

#=========================================================================
#Client
def sendFileFromServer(filename):
    s = socket(AF_INET,SOCK_DGRAM) #소캣 32bit UDP
    addr = (HOST,PORT) 
    print(s.connect(addr))
    f=open (filename, "rb") #파일 일기용으로 열기
    data = f.read(BUFSIZE) #파일 읽기
    while (data): 
        if(s.sendto(data,addr)): #파일 내용 전송
         print ("uploading ...") 
         data = f.read(BUFSIZE) 
    s.close()
    f.close()
    
def client():
    filename = input('업로드 할 파일이름을 입력하세요:')
    sendFileFromServer(filename)


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
        server()
    # 첫 매개변수가 '-c' 라면
    elif sys.argv[1] == '-c':
        #클라이언트 함수 호출
        client()
__main__()
