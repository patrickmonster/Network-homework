import socket
import socketserver
import threading
import datetime
import random
from struct import *
import rsa

HOST = ''
PORT = 9000
lock = threading.Lock() # syncronized 동기화 진행하는 스레드 생성

def get_time_ms():
    return round(datetime.datetime.utcnow().timestamp() * 1000)



userid = None
count = 0
class UserManager:
    def __init__(self,index):
        self.users = {}
    def addID(self, id,data, conn, addr): # 사용자 ID를 self.users에 추가하는 함수
        #if id in self.users: # 이미 등록된 사용자라면
        #    return None
        
        # 새로운 사용자를 등록함
        lock.acquire() # 스레드 동기화를 막기위한 락
        self.users[id] = (conn, addr,data)
        lock.release() # 업데이트 후 락 해제
        print("사용자 등록:",addr,"\tid:",id,"\t데이터:",data)
            
    def removeID(self, id): #사용자를 제거하는 함수
        if id not in self.users:
            return
        lock.acquire()
        self.dv.removeNode(id)
        del self.users[id]
        lock.release()
        print('노드제거완료 :', self.dv)
      #self.sendMessageToAll('[%s]님이 퇴장했습니다.' %username)
      #print('--- 대화 참여자 수 [%d]' %len(self.users))
    def getUsers(self):
        return self.users

#메인 스레드
class MyTcpHandler(socketserver.BaseRequestHandler):

    def handle(self):
        print('[%s] 연결됨' %self.client_address[0])
        id = ''
        try:
            n,e,d = rsa.getRsa()
            while n in userid.getUsers().keys():
                n,e,d = rsa.getRsa()
            userid.addID(n,(n,e,d),self.request,self.client_address)#사용자 추가
            s = "N" + str(n).zfill(6) + str(e).zfill(6) #퍼블릭키 전송
            self.request.send(s.encode())
            msg = self.request.recv(1024)
            while msg:
                userid.messageHandler(n,(e,d),mag.decode())
            self.request.recv(1024)
            msg = self.request.recv(1024)
            time = get_time_ms() - int(msg[3:]) + random.randrange(10,30) #경과 시간#1559256979969 # .zfill(5) / 5자리 맞추기
            userid.addID(id,time,self.request,self.client_address)#사용자 추가
            msg = self.request.recv(1024)
            while msg:
                print("수신된 암호문 :",msg.decode())#수신된 메세지 출력
                print("수신된 평문   :",rsa.decrypt((d,n), msg.decode()))
                msg = self.request.recv(1024)
        except KeyboardInterrupt as e:
        #except Exception as e:
            print(e)
        
        print('[%s] 접속종료' %self.client_address[0])
        
        userid.removeID(id)
    def registerID(self):
        
        pass
        #while True:
            
            #self.request.send('로그인ID:'.encode())
            #username = self.request.recv(1024)
            #username = username.decode().strip()
            #if self.userman.addUser(username, self.request, self.client_address):
                #return username
    
class ChatingServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def runServer(port):
   print('+++ DV 서버를 시작합니다.')
   print('+++ DV 서버를 끝내려면 Ctrl-C를 누르세요.')
   
   try:
      server = ChatingServer(('', port), MyTcpHandler)
      server.serve_forever()
   except KeyboardInterrupt:
      print('--- DV 서버를 종료합니다.')
      server.shutdown()
      server.server_close()

def rcvMsg(sock,callback):
   while True:
      try:
         data = sock.recv(1024)
         if not data:
            break
         print("수신된 데이터:",data.decode())
      except:
         pass
def runClient(host,port):
    def callback(msg):
        pass
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host,port))
        t = threading.Thread(target=rcvMsg, args=(sock,callback))
        t.daemon = True
        t.start()
        while True:
            msg = input()
            sock.send(msg.encode())
decimals = rsa.getS() #소수 집합
s = None
def run(port):
    c = input("c ? s ? :")
    if c in 'c':
        s = input('Host :')
        runClient(s,port)
    else:
        runServer(port)
index = int(input('포트번호 :'))
userid = UserManager(index)
run(index)
