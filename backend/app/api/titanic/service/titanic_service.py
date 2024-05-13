
from app.api.titanic.model.titanic_model import TitanicModel
import pandas as pd




class TitanicService:

    model = TitanicModel() 

    def process(self):
        print(f'프로세스 시작')
        this = self.model
        this.train = self.new_model('train.csv')
        this.test = self.new_model('test.csv')
    
        self.df_info(this)
        
        # print(f'트레인 컬럼 : {this.train.columns}')
        # print(f'테스트 컬럼 : {this.test.columns}')
        this.id=this.test['PassengerId']
        self.drop_feature(this,'Ticket','Cabin','SibSp','Parch','Name')
  
        self.df_info(this)
        
        
        this = self.create_train(this)
        
    @staticmethod
    def drop_feature(this, *feature) -> object: #f*은 여러개를 받을 수 있다.

        
        # for i in feature:
        #     this.train = this.train.drop([i], axis=1)
        #     this.test = this.test.drop(i, axis=1)
            
        # for i in [this.train, this.test]:
        #    for j in feature:
        #        i.drop(j, axis=1, inplace=True)
               
        [i.drop(j, axis=1, inplace=True) for j in feature for i in [this.train, this.test]] 
        
        return this
        
        
    @staticmethod
    def df_info(this):
           
        [print(f'{i}') for i in [this.train, this.test] ] 
            
        
        
    

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



    
    
