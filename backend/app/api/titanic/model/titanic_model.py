from dataclasses import dataclass
import numpy as np
import pandas as pd

from icecream import ic
from sklearn import linear_model, naive_bayes, svm
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import KFold, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from app.api.context.data_sets import DataSets
from app.api.context.models import Models


class TitanicModel(pd.DataFrame):

    model = Models()
    dataset = DataSets()

    def preprocess(self, train_fname, test_fname) -> pd.DataFrame:

        ic(f'--- TitanicModel 전처리 시작 ----')
        this =  self.dataset
        that = self.model
        ic(this)
        ic(that)
        feature = ['PassengerId', 'Survived', 'Pclass', 'Name', 'Sex', 'Age', 'SibSp', 'Parch', 'Ticket', 'Fare', 'Cabin', 'Embarked']
        # 데이터셋은 Train과 Test, Validation 3종류로 나뉘어져 있다.
        this.train = that.new_dataframe_no_index(f'{train_fname}')
        this.test = that.new_dataframe_no_index(f'{test_fname}')
        this.id = this.test['PassengerId']
        this.label = this.train['Survived']
        this.train = this.train.drop('Survived', axis=1)
        this = self.drop_feature(this,'SibSp', 'Parch', 'Cabin', 'Ticket')
        # this = self.drop_feature(this, 'SibSp', 'Parch', 'Cabin', 'Ticket')
        this = self.extract_title_from_name(this)
        title_mapping = self.remove_duplicate_title(this)
        this = self.title_nominal(this, title_mapping)
        this = self.drop_feature(this, 'Name')
        this = self.sex_nominal(this)
        this = self.drop_feature(this, 'Sex')
        this = self.embarked_nominal(this)  
        self.df_info(this)
        this = self.age_ratio(this)
        this = self.drop_feature(this, 'Age')
        this = self.pclass_ordinal(this)
        this = self.fare_ratio(this)
        this = self.drop_feature(this, "Fare")
       
        
        # self.learning(this)
        
        
        self.df_info(this)
        
        k_fold = self.create_k_fold()
        accuracy = self.get_accuracy(this, k_fold)
        accuracy2 = self.get_accuracy2(this, k_fold)
        accuracy3 = self.get_accuracy3(this, k_fold)
        accuracy4 = self.get_accuracy4(this, k_fold)
        # accuracy5 = self.get_accuracy5(this, k_fold)
        accuracy6 = self.get_accuracy6(this, k_fold)
        
        print(f'랜덤포레스트 정확도: {accuracy} ') 
        print(f'KNN 정확도: {accuracy2}')
        print(f'SVM 정확도: {accuracy3}')
        print(f'로지스틱 정확도: {accuracy4}')
        # print(f'KMeans  정확도: {accuracy5}')
        print(f'의사결정트리 정확도: {accuracy6}')
 

        return this

    def df_info(self, this):
        print('*' * 50)
        print(f'1. Train 의 type 은 {type(this.train)} 이다.')
        print(f'2. Train 의 column 은 {this.train.columns} 이다.')
        print(f'3. Train 의 상위 1개의 데이터는 {this.train.head()} 이다.')
        print(f'4. Train 의 null 의 갯수는 {this.train.isnull().sum()} 이다.')
        print(f'5. Test 의 type 은 {type(this.test)} 이다.')
        print(f'6. Test 의 column 은 {this.test.columns} 이다.')
        print(f'7. Test 의 상위 1개의 데이터는 {this.test.head()} 이다.')
        print(f'8. Test 의 null 의 갯수는 {this.test.isnull().sum()} 이다.')

    @staticmethod
    def drop_feature(this, *feature) -> object:
        ic(type(feature))
        # for i in feature:
        #     this.train = this.train.drop([i], axis=1)
        #     this.test = this.test.drop(i, axis=1)

        # for i in [this.train, this.test]:
        #     for j in feature:
        #         i.drop(j, axis=1, inplace=True)

        [i.drop(j, axis=1, inplace=True) for j in feature for i in [this.train, this.test]]

        return this

    @staticmethod
    def extract_title_from_name(this) -> pd.DataFrame:
        combine = [this.train, this.test]
        for i in combine:
            i['Title'] = i['Name'].str.extract(
                '([A-Za-z]+)\.', expand=False)  #
        return this

    @staticmethod
    def remove_duplicate_title(this) -> pd.DataFrame:
        a = []
        for these in [this.train, this.test]:
            a += list(set(these['Title']))
        a = list(set(a))
        print(a)

        '''
        ['Mr', 'Sir', 'Major', 'Don', 'Rev', 'Countess', 'Lady', 'Jonkheer', 'Dr',
        'Miss', 'Col', 'Ms', 'Dona', 'Mlle', 'Mme', 'Mrs', 'Master', 'Capt']
        Royal : ['Countess', 'Lady', 'Sir']
        Rare : ['Capt','Col','Don','Dr','Major','Rev','Jonkheer','Dona','Mme' ]
        Mr : ['Mlle']
        Ms : ['Miss']
        Master
        Mrs
        '''
        title_mapping = {'Mr': 1, 'Ms': 2, 'Mrs': 3,
                         'Master': 4, 'Royal': 5, 'Rare': 6}

        return title_mapping

    @staticmethod
    def title_nominal(this, title_mapping) -> pd.DataFrame:

        for these in [this.train, this.test]:
            these['Title'] = these['Title'].replace(
                ['Countess', 'Lady', 'Sir'], 'Royal')
            these['Title'] = these['Title'].replace(
                ['Capt', 'Col', 'Don', 'Dr', 'Major', 'Rev', 'Jonkheer', 'Dona', 'Mme'], 'Rare')
            these['Title'] = these['Title'].replace(['Mlle'], 'Mr')
            these['Title'] = these['Title'].replace(['Miss'], 'Ms')
            # Master 는 변화없음
            # Mrs 는 변화없음
            these['Title'] = these['Title'].fillna(0)
            these['Title'] = these['Title'].map(title_mapping)

        return this

    @staticmethod
    def age_ratio(this) -> pd.DataFrame:
        train = this.train
        test = this.test
        age_mapping = {'Unknown': 0, 'Baby': 1, 'Child': 2, 'Teenager': 3, 'Student': 4,
                       'Young Adult': 5, 'Adult': 6,  'Senior': 7}
        train['Age'] = train['Age'].fillna(-0.5)
        test['Age'] = test['Age'].fillna(-0.5)  # 왜 NaN 값에 -0.5 를 할당할까요 ?
        bins = [-1, 0, 5, 12, 18, 24, 35, 60, np.inf]
        labels = ['Unknown', 'Baby', 'Child', 'Teenager',
                  'Student', 'Young Adult', 'Adult', 'Senior']

        for these in train, test:
            pass  # pd.cut() 함수를 이용하여 Age를 구간화 하세요
            these['Age'] = pd.cut(these['Age'], bins, labels=labels)
            these['AgeGroup'] = these['Age'].map(age_mapping)

        return this

    @staticmethod
    def sex_nominal(this) -> pd.DataFrame:
        gender_mapping = {'male': 0, 'female': 1}
        for these in [this.train, this.test]:
            these['Gender'] = these['Sex'].map(gender_mapping)  # 'Sex' 열을 'gender'로 변경
        return this

    @staticmethod
    def embarked_nominal(this) -> pd.DataFrame:

        for these in [this.train, this.test]:
            these['Embarked'] = these['Embarked'].fillna('S')  # fill
            these['Embarked'] = these['Embarked'].map(
                {'S': 0, 'C': 1, 'Q': 2})  # map을 안써? -> map을 쓰면 원하는 값으로 변환 가능
        return this

    @staticmethod
    def fare_ratio(this) -> pd.DataFrame:
        bins = [-1, 0, 8, 15, 31, np.inf]
        labels = ['Unknown', '1_quartile',
                  '2_quartile', '3_quartile', '4_quartile']

        for these in [this.train, this.test]:
            these['FareBand'] = pd.cut(these['Fare'], bins, labels=labels)
            these['FareBand'] = these['FareBand'].map(
                {'Unknown': 0, '1_quartile': 1, '2_quartile': 2, '3_quartile': 3, '4_quartile': 4})
        return this

    @staticmethod
    def create_k_fold() -> object:
        return KFold(n_splits=10, shuffle=True, random_state=0)

    @staticmethod
    def learning(self, train_fname, test_fname) -> object:
        this = self.preprocess(train_fname, test_fname)
        print(f'학습 시작')
        k_fold = self.create_k_fold()
        accuracy = self.get_accuracy(this, k_fold)
        print(f'사이킷런 알고리즘 정확도: {accuracy}')
        return accuracy

    @staticmethod
    def get_accuracy(this, k_fold) -> object:
        score = cross_val_score(RandomForestClassifier(
        ), this.train, this.label, cv=k_fold, n_jobs=1, scoring='accuracy') 
    
        return round(np.mean(score)*100, 2)

    @staticmethod
    def get_accuracy2(this, k_fold) -> object:
        score = cross_val_score(KNeighborsClassifier(
        ), this.train, this.label, cv=k_fold, n_jobs=1, scoring='accuracy') 
        return round(np.mean(score)*100, 2)
    
    @staticmethod
    def get_accuracy3(this, k_fold) -> object:
        score = cross_val_score(svm.SVC(
        ), this.train, this.label, cv=k_fold, n_jobs=1, scoring='accuracy') 
        return round(np.mean(score)*100, 2)
    
    @staticmethod
    def get_accuracy4(this, k_fold) -> object:
        score = cross_val_score(linear_model.LogisticRegression(
        ), this.train, this.label, cv=k_fold, n_jobs=1, scoring='accuracy') 
        return round(np.mean(score)*100, 2)
    
    # @staticmethod
    # def get_accuracy5(this, k_fold) -> object:
    #     score = cross_val_score(KMeans (
    #     ), this.train, this.label, cv=k_fold, n_jobs=1, scoring='accuracy') 
    #     return round(np.mean(score)*100, 2)
    
    @staticmethod
    def get_accuracy6(this, k_fold) -> object:
        score = cross_val_score(DecisionTreeClassifier(
        ), this.train, this.label, cv=k_fold, n_jobs=1, scoring='accuracy') 
        return round(np.mean(score)*100, 2)

    
    @staticmethod
    def pclass_ordinal(this) -> pd.DataFrame:
        pclass_mapping = {1: '1', 2: '2', 3: '3'}
        for these in [this.train, this.test]:
            these['Pclass'] = these['Pclass'].map(pclass_mapping)
        return this