#!/usr/bin/env python

# TCP 통신 예제 파일전송
import socket
import sys
import socketserver
from os.path import exists

HOST = 'localhost'
PORT = 80
BUFSIZE = 1024
#=========================================================================
#Server
class MyTcpHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data_transferred = 0
        print('[%s] 연결됨' %self.client_address[0])
        filename = self.request.recv(1024) # 클라이언트로 부터 파일이름을 전달받음
        filename = filename.decode() # 파일이름 이진 바이트 스트림 데이터를 일반 문자열로 변환
 
        if not exists(filename): # 파일이 해당 디렉터리에 존재하지 않으면
            print("요청파일[%s]" %filename)
            return # handle()함수를 빠져 나온다.
 
        print('파일[%s] 전송 시작...' %filename)
        with open(filename, 'rb') as f:
            try:
                data = f.read(1024) # 파일을 1024바이트 읽음
                while data: # 파일이 빈 문자열일때까지 반복
                    data_transferred += self.request.send(data)
                    data = f.read(1024)
            except Exception as e:
                print(e)
 
        print('전송완료[%s], 전송량[%d]' %(filename,data_transferred))
 
 
def server():
    print('++++++파일 서버를 시작++++++')
    print("+++파일 서버를 끝내려면 'Ctrl + C'를 누르세요.")
 
    try:
        server = socketserver.TCPServer((HOST,PORT),MyTcpHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print('++++++파일 서버를 종료합니다.++++++')

#=========================================================================
#Client
def getFileFromServer(filename):
    data_transferred = 0
 
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST,PORT))
        sock.sendall(filename.encode())
 
        data = sock.recv(1024)
        if not data:
            print('파일[%s]: 서버에 존재하지 않거나 전송중 오류발생' %filename)
            return
        if len(sys.argv) >= 3:
            filename = sys.argv[3];
        else: filename += "_tmp.txt"
        with open(filename,'wb') as f:
            try:
                while  data:
                    f.write(data)
                    data_transferred += len(data)
                    data = sock.recv(1024)
            except Exception as e:
                print(e)
 
    print('파일[%s] 전송종료. 전송량 [%d]' %(filename, data_transferred))
def client():
    filename = input('다운로드 받은 파일이름을 입력하세요:')
    getFileFromServer(filename)


#=========================================================================

def usage():
    sys.stdout = sys.stderr
    print ('Usage: python FileTCP.py -s [port]            (server)')
    print ('or:    python FileTCP.py -c host [port] [fileName] <file (client)')
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
