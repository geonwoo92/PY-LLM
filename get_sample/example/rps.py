import random


# class RPS:

#     def __init__(self) -> None:
#         print(f'utils.py myRandom() 를 이용하여 가위바위보 객체를 생성합니다')

def myRandom(start, end): return random.randint(start, end-1)


if __name__ == '__main__':
    c = myRandom(1, 4)
    p = input('1', '2', '3')
    if p == '1':
        you = '가위'
    elif p == '2':
        you = '바위'
    else:
        you = '보'

    rps = ['가위', '바위', '보']
    if you == rps[c-1]:
        print(f'컴퓨터: {rps[c-1]} 당신: {you} 비겼습니다') # 0, 1, 2
    elif you == rps[c % 3]:
        print(f'컴퓨터: {rps[c-1]} 당신: {you} 이겼습니다') # 1, 2, 0     
    else:
        print(f'컴퓨터: {rps[c-1]} 당신: {you} 졌습니다') # 2, 0, 1
