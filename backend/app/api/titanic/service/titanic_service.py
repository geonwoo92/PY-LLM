
from app.api.titanic.model.titanic_model import TitanicModel
import pandas as pd


class TitanicService:

    model = TitanicModel() 

    def process(self):
        print(f'프로세스 시작')
        train_model = self.new_model('train.csv')
        test_model = self.new_model('test.csv')
        print(f'트레인 컬럼 : {train_model.columns}')
        print(f'테스트 컬럼 : {test_model.columns}')

    def new_model(self, playload) -> object:
        this = self.model
        this.context = './app/api/titanic/data/'
        this.fname = playload
        return pd.read_csv(this.context + this.fname)
    
    @staticmethod #훈련센터
    def create_train(this) -> str:
        return this.train.drop('Survived',axis=1) # 0:행, 1:열

    @staticmethod #테스트센터
    def create_label(this) -> str:
        return this.train['Survived'] 

    @staticmethod
    def drop_feature(this, *feature) -> object:
        for i in feature:
            pass
        

    
    
