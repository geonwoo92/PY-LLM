
from app.api.titanic.model.titanic_model import TitanicModel
import pandas as pd


class TitanicService:

    model = TitanicModel()

    def process(self):
        print(f'프로세스 시작')
        this = self.model
        this.train = self.new_model('train.csv')
        this.test = self.new_model('test.csv')
        feacture = ['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex',
                    'Age', 'SibSp', 'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked']

        self.df_info(this)

        this.id = this.test['PassengerId']

        this = self.name_nominal(this)
        this = self.drop_feature(
            this, 'Ticket', 'Cabin', 'SibSp', 'Parch', 'Name')
        this = self.age_ratio(this)
        this = self.fare_ratio(this)
        this = self.pclass_ordinal(this)
        this = self.embarked_nominal(this)
        this = self.sex_nominal(this)

        self.df_info(this)

        this = self.create_train(this)



    @staticmethod
    def df_info(this):

        [print(f'{i}') for i in [this.train, this.test]]  # 리스트 컴프리헨션

    @staticmethod  # 훈련센터
    def create_train(this) -> str:
        return this.train.drop('Survived', axis=1)  # 0:행, 1:열

    @staticmethod  # 테스트센터
    def create_label(this) -> str:
        return this.train['Survived']

    @staticmethod
    def embarked_nominal(this) -> object:
        this.train = this.train.fillna({'Embarked': 'S'})
        this.test = this.test.fillna({'Embarked': 'S'})
        this.train['Embarked'] = this.train['Embarked'].map(
            {'S': 1, 'C': 2, 'Q': 3})
        this.test['Embarked'] = this.test['Embarked'].map(
            {'S': 1, 'C': 2, 'Q': 3})
        return this

    @staticmethod
    def pclass_ordinal(this) -> object:
        this.train['Pclass'] = this.train['Pclass'].map({1: 1, 2: 2, 3: 3})
        this.test['Pclass'] = this.test['Pclass'].map({1: 1, 2: 2, 3: 3})
        return this

    @staticmethod
    def fare_ratio(this) -> object:
        for data in [this.train, this.test]:
            data['Fare'] = data['Fare'].fillna(0)
            data['Fare'] = data['Fare'] // 10
        return this

    @staticmethod
    def name_nominal(this) -> object:
        for data in [this.train, this.test]:
            data['Name'] = data['Name'].map(
                lambda x: x.split(',')[1].split('.')[0].strip())
            data['Name'] = data['Name'].map({
                'Capt': 1, 'Col': 2, 'Don': 3, 'Dr': 4,
                'Jonkheer': 5, 'Lady': 6, 'Major': 7,
                'Master': 8, 'Miss': 9, 'Mlle': 10, 'Mme': 11,
                'Mr': 12, 'Mrs': 13, 'Ms': 14, 'Rev': 15, 'Sir': 16, 'the Countess': 17
            })
        return this

    @staticmethod
    def age_ratio(this) -> object:
        for data in [this.train, this.test]:
            data['Age'] = data['Age'].fillna(0)
            data['Age'] = data['Age'] // 10
        return this

    @staticmethod
    def extract_title(this) -> object:
        combine = [this.train, this.test]
        for i in combine:
            i['Title'] = i.Name.str.extract('([A-Za-z]+)\.', expand=False)
        return this
