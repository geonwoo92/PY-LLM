
import pandas as pd
from app.api.context.data_sets import DataSets


class Models:
    def __init__(self) -> None:
        self.ds = DataSets()
        this = self.ds
        this.dname = './app/api/context/data/'  # 데이터 저장소
        this.sname = './app/api/context/save/'  # 모델 저장소


    def new_dataframe_with_index(self, fname: pd.DataFrame) -> pd.DataFrame:
        this = self.ds
        # index_col=0 해야 기존 index 값이 유지된다
        # 0 은 컬럼명 중에서 첫번째를 의미한다(배열구조)
        # pd.read_csv(f'경로/파일명/csv', index_col=0 = '인덱스로 지정할 column 명') Index 지정

     
        return pd.read_csv(f'{this.dname}{fname}', index_col=0)
    
    
    def new_dataframe_no_index(self, fname: str) -> object:
        this = self.ds
        # pd.read_csv('경로/파일명.csv') Index 를 지정하지 않음
        return pd.read_csv(f'{this.dname}{fname}')
    
    def save_model(self, fname, dframe: pd.DataFrame) -> pd.DataFrame:
        this = self.ds

        '''
        풀옵션은 다음과 같다
        df.to_csv(f'{self.dname}{fname}.csv', sep=',', na_rep='NaN',
        float_format='%.2f', # 2 decimal places columns=['ID', 'X2'],
        # columns to write index=false) # do not write index
        '''
        
        return pd.to_csv(f'{this.sname}{fname}',sep=',', na_rep ='NaN') 