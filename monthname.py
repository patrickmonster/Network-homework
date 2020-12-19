def getMN(m):
    mn = {
        1:"Januay",2:'February',3:'March',4:'April',5:'May',6:'June',
        7:'July',8:'August',9:'September', 10:'October',11:'November',12:'December'
        }
    try:
        r = mn[m]
    except:
        r = 'Please Inut Month Between 1~12'
    return r

if __name__ == '__main__':
    print('이건 모듈, 다른곳에서 임포트해라')
