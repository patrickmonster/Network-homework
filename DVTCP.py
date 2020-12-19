#-*- coding: utf-8 -*-


import socket
import sys
import socketserver

import datetime


HOST = 'localhost'
BUFSIZE = 1024


def get_epochtime_ms():
    return round(datetime.datetime.utcnow().timestamp() * 1000)

class DV(list):

    #현재 알고리즘 적용 네트워킹 id값
    def __init__(s,index):
        s.i = index
        for i in range(index):#현재 노드를 기준으로 하위 노드를 추가
            s.append([-1 for j in range(index+1)])#빈 상태를 추가시킴 (모든 거리 무한으로)
        s.N = [randrange(1,20) for i in range(index)]#0~100 - 현재 노드에서의 거리
        s.N.append(0) #현재 노드에서 현재노드까지의 거리는 0
        print(s.i,'노드상태:',s.N)
        s.append(s.N)#현재 노드도 추가
        
    def addNet(s,connect = True):
        #네트워크 상태를 추가시킴
        print('처리전:',s)
        print(s.i,"노드추가 :",connect)
        for i in range(len(s)):
            s[i].append(-1)
        s.N[len(s)] = randrange(1,20) #추가된 노드까지의 거리를 추가
        s.append([-1 for j in range(len(s)+1)])
        print('처리결과:',s)
        
    def addNets(s,connects):
        ss = len(s)
        for i in range(len(connects)):
            s.addNet(ss+i,connect = connects[i])
        print("추가 완료! 크기:",len(s))
        
    #수신  -> 전송받은 번지와 데이터6값
    def recv(s,index, data):
        up = False
        s[index] = data #노드 거리 벡터값 초기화
        
        #연결된 모든 노드를 탐색
        #i번지 까지 가4는 경로를 탐색
        for i in range(len(s)):#s.N 의 노드를 재 탐색
            if i == s.i:#i번지와 현재 index 가 같다면 생략
                continue 
            #i번지의 i에서 부터 index로 가는길과 바로 
            for j in range(len(s[i])):
                if s[j][i] == -1 or s.N[j] == -1:
                    continue
                if s[j][i]+s.N[j] < s.N[i] or s.N[i] == -1:
                    print(s.i,'정렬',s.N[i],'->(',str(j),',',str(i),')',s[j][i]+s.N[j])
                    s.N[i] = s[j][i]+s.N[j]
                    up = True

        print("정렬 완료",s.i)
        return up #업데이트 여부
    def send(s):
        out = []
        for i in s.N:
            out.append(i)
        print('복사:',out)
        return out
    
    def __repr__(s):
        out = '(' + str(s.i) + ')\n'
        index = 0
        for i in s:
            out += str(index) + str(i) + '\n'
            index+= 1
        return out

class TcpHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print('[%s] 연결됨' %self.client_address[0])
        data = self.request.recv(1024) # 클라이언트로 부터 파일이름을 전달받음
        while True:
            tt = get_epochtime_ms()#전송받는데 현재 시간
            
            readBuf = c_sock.recv(BUFSIZE) 
            if len(readBuf) == 0:
                break
            print('클라이언트 전송시간: ', int(readBuf.decode()) - tt)
            self.request.send(str(get_epochtime_ms()))#전송 시간 전송
        

def server(port=80):
    print('++++++DV 서버를 시작++++++')
    print("+++DV 서버를 끝내려면 'Ctrl + C'를 누르세요.")
    try:
        server = socket.TCPServer((HOST,port),TcpHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print('++ ++++DV 서버를 종료합니다.++++++')
def client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind('',0)
        print('서버 연결 ')
        sock.send(str(get_epochtime_ms()))#현재 시각 전송

        tt = get_epochtime_ms() - int(sock.recv(1024))

        print('전송에 걸린 시간: ',tt)

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
