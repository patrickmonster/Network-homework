#-*- coding: utf-8 -*-

#난수 생성기
from random import *

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


'''
max = 3
c = []
for i in range(max):
    for j in c:
        j.addNet(choice([True, False]))
    c.append(DV(i))

print(c)
print('0 <- 1')
c[0].recv(1,c[1].send())
c[0].recv(2,c[2].send())

c[1].recv(0,c[0].send())
c[1].recv(2,c[2].send())

c[2].recv(0,c[0].send())
c[2].recv(1,c[1].send())
print(c)
'''
