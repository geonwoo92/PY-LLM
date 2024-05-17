from example.utils import Member, myRandom


class BMI():
    def __init__(self) -> None:
        '''utils.py / Member(), myRandom() 를 이용하여 BMI 지수를 구하는 계산기를 작성합니다.'''
    
    
    this = Member()
    this.name = '홍길동'
    this.height = myRandom(160, 180)
    this.weight = myRandom(50, 90)
    res = this.weight / (this.height/100)**2 
    print(f'{this.name}님의 BMI 지수는 {res:.2f}입니다')