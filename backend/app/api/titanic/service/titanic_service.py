
from app.api.titanic.model.titanic_model import TitanicModel
import pandas as pd


class TitanicService:

    model = TitanicModel() 

    def new_model(self, playload) -> object:
        this = self.model
        this.context = '../data/'
        this.fname = playload
        return pd.read_csv(this.context + this.fname)
        


    
        

