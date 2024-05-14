
import pandas as pd
from app.api.context.data_sets import DataSets


class Models:
    def __init__(self) -> None:
        self.ds = DataSets()
        this = self.ds
        this.dname = './data/'  # 데이터 저장소
        this.sname = './save/'  # 모델 저장소


    def new_model(self, fname) -> object:
        this = self.ds
        # index_col=0은 인덱스를 0으로 설정 해야 기존 인덱스 값이 유지된다.
        # 0은 컬럼명 중에서 첫번째 컬럼을 인덱스로 사용하겠다는 의미(배열구조)
        # pd.read_csv(f'경로/파일명/csv',index_col=0 = ' 인덱스로 지정할 cloumn명') Index 지정

        return pd.read_csv(f'{this.dname}{fname}', index_col=0)  # 인덱스를 0으로 설정
    
    
    def new_dframe(self, fname) -> object:
        this = self.ds
        # pd.read_csv(f'경로/파일명/csv') Index 를 지정하지 않음
        
        return pd.DataFrame(f'{this.dname}{fname}')  # 인덱스를 0으로 설정
    
    def save_model(self, fname, dframe) -> object:
        this = self.ds

        '''
        풀옵션은 다음과 같다
        df.to_csv(f'{self.dname}{fname}.csv', sep=',', na_rep='NaN',
        float_format='%.2f', # 2 decimal places columns=['ID', 'X2'],
        # columns to write index=false) # do not write index
        '''
        
        return pd.to_csv(f'{this.sname}{fname}',sep=',', na_rep ='NaN') 