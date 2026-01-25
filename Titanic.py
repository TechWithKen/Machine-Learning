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

pipeline_mod.fit(titanic_ship, survived)


titanic_test = pd.read_csv("./test.csv")
titanic_test.drop(columns=["PassengerId", "Name", "Ticket", "Fare", "Cabin"], inplace=True)
titanic_test.shape, titanic_ship.shape

survived_passengers = pipeline_mod.predict(titanic_test)

submission = pd.DataFrame({
    "PassengerId": pd.read_csv("./test.csv")["PassengerId"],
    "Survived": survived_passengers
})
