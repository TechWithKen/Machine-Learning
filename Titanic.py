import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.impute import SimpleImputer


def titanic_data():
    titanic_ship = pd.read_csv("./train.csv")
    survived = titanic_ship["Survived"]
    titanic_ship.drop(columns=["Survived","PassengerId", "Name", "Ticket", "Fare", "Cabin"], inplace=True)

    return {"titanic_ship": titanic_ship, "survived": survived}



def train_model():
    data = titanic_data()
    category_feature = ["Sex", "Embarked"]
    num_features = ["Pclass", "Age", "SibSp", "Parch"]


    preprocessing = ColumnTransformer(transformers=[
        ("cat", Pipeline(steps=[("imputer", SimpleImputer(strategy="most_frequent")),
                        ("encoder", OneHotEncoder(drop="first", sparse_output=False))]), category_feature),
        ("num", Pipeline(steps=[("imputer", SimpleImputer(strategy="median"))]), num_features)

    ], remainder="passthrough")


    pipeline_mod = Pipeline(steps=[
        ("preprocess", preprocessing),
        ("model", LogisticRegression())
    ])

    pipeline_mod.fit(data["titanic_ship"], data["survived"])

    return pipeline_mod


def test_dataset():
    trained_model = train_model()
    titanic_test = pd.read_csv("./test.csv")
    titanic_test.drop(columns=["PassengerId", "Name", "Ticket", "Fare", "Cabin"], inplace=True)

    survived_passengers = trained_model.predict(titanic_test)

    return survived_passengers


print(test_dataset())
