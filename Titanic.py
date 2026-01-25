import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.impute import SimpleImputer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score


def titanic_data():
    titanic_ship = pd.read_csv("./train.csv")
    survived = titanic_ship["Survived"]
    titanic_ship.drop(columns=["Survived","PassengerId", "Name", "Ticket", "Fare", "Cabin"], inplace=True)

    return {"titanic_ship": titanic_ship, "survived": survived}



def train_model(model):
    category_feature = ["Sex", "Embarked"]
    num_features = ["Pclass", "Age", "SibSp", "Parch"]


    preprocessing = ColumnTransformer(transformers=[
        ("cat", Pipeline(steps=[("imputer", SimpleImputer(strategy="most_frequent")),
                        ("encoder", OneHotEncoder(drop="first", sparse_output=False))]), category_feature),
        ("num", Pipeline(steps=[("imputer", SimpleImputer(strategy="median"))]), num_features)

    ], remainder="passthrough")


    pipeline_mod = Pipeline(steps=[
        ("preprocess", preprocessing),
        ("model", model)
    ])

    return pipeline_mod


def evaluate_model():
    data = titanic_data()

    models = {
        "LogisticsRegression": LogisticRegression(class_weight="balanced"),
        "KNearestNeighbours": KNeighborsClassifier(),
        "RandomForest": RandomForestClassifier(),
    }
    best_score = 0
    best_name = ""
    best_model = None

    for name, model in models.items():
        pipeline = train_model(model)
        score = cross_val_score(pipeline, data["titanic_ship"], data["survived"], cv=6).mean()
        if score > best_score:
            best_score = score
            best_name = name
            best_model = pipeline

    print("Best Model:", best_name)
    print("Best Score:", best_score)
    return best_model


def test_dataset():
    trained_model = evaluate_model()
    trained_model.fit(titanic_data()["titanic_ship"], titanic_data()["survived"])
    titanic_test = pd.read_csv("./test.csv")
    passenger_id = titanic_test["PassengerId"]
    titanic_test.drop(columns=["PassengerId", "Name", "Ticket", "Fare", "Cabin"], inplace=True)

    survived_passengers = trained_model.predict(titanic_test)
    new_titanic_data = pd.DataFrame(survived_passengers)
    new_titanic_data = pd.concat([passenger_id, new_titanic_data], axis=1)
    new_titanic_data.rename(columns={0: "Survived"}, inplace=True)
    new_titanic_data = new_titanic_data.to_csv("new_titanic1.csv", index=False)
    
    return new_titanic_data


print(test_dataset())
