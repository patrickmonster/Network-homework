#-*- coding: utf-8 -*-

#난수 생성기
from random import *

#다익스트라 알고리즘 처리기
#api 사용 안하기 프로젝트

def findSort(거리,통과지점):
    min = 9999
    index = 0
    for i in range(len(거리)):
        if 통과지점[i]:
            continue
        if 거리[i] < min:
            min = 거리[i]
            index = i
    return index

def Dijkstra(비용, 시작지점):
    거리 = [0 for i in range(len(비용))]
    #탐색여부
    s = [0 for i in range(len(비용))]
    #경로
    r = [0 for i in range(len(비용))]
    
    for i in range(len(비용)):
        거리[i] = 비용[시작지점][i]
    s[시작지점] = 1
    거리[시작지점 ] = 0
    for i in range(1,len(비용)):
        u = findSort(거리,s)
        """
        print("최소거리 : " + str(u))
        print("경로 : " + str(r))
        print("거리 : " + str(거리))
        print("비교 : " + str(비용[u]))
        print("탐색 : " + str(s))
        """
        s[u] = 1
        for j in range(len(비용)):
            if s[j] == 1:
                continue
            if (거리[j] > 거리[u] + 비용[u][j]):
                print("변경(" + str(j) + ")" + str(r[u]) + "에서"+str(u) + " 변경값 = " + str(거리[j]) +"에서" + str(거리[u] + 비용[u][j]))
                거리[j] = 거리[u] + 비용[u][j]
                r[j] = u
        
        print("="*50)
    return (r, 거리)

n = 20

비용 = list()
for i in range(n):
    tmp = []
    for j in range(n) :
        tmp.append(randrange(1,51))
    비용.append(tmp)

for i in 비용:
    print(str(i))
print("="*50)

j ,k = Dijkstra(비용,0)
print("="*50)
print("경로")
print(j)
print("="*50)
print("최단거리")
print(k)
