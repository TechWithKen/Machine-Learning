import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, KBinsDiscretizer, StandardScaler, MaxAbsScaler, MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.impute import SimpleImputer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from xgboost import XGBClassifier
from category_encoders import TargetEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score


titanic_ship = pd.read_csv("./train.csv")
survived = titanic_ship["Survived"]
titanic_ship.drop(columns=["Survived","PassengerId", "Name", "Ticket"], inplace=True)
X = titanic_ship
y = survived

category_feature = ["Sex", "Embarked"]
target_features = ["Cabin"]
num_features = ["Pclass", "Age", "SibSp", "Parch", "Fare"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)
preprocessing = ColumnTransformer(transformers=[
    ("cat", Pipeline(steps=[("imputer", SimpleImputer(strategy="most_frequent")),
                    ("encoder", OneHotEncoder(drop="first", sparse_output=False))]), category_feature),
    ("num", Pipeline(steps=[("imputer", SimpleImputer(strategy="median")), 
                            ("scaler", MinMaxScaler())]), num_features),
    ('tar', TargetEncoder(), target_features)

], remainder="passthrough")


base_model = [
    ('xgb', XGBClassifier(n_estimators=200, learning_rate=0.8, random_state=42, subsample=1.0, max_depth=3)),
    ("rdf", RandomForestClassifier(n_estimators=100, criterion="gini", max_depth=5, max_features="sqrt", max_leaf_nodes=2, random_state=42)),
    ("svm", SVC(probability=True, C=0.1, kernel="rbf", gamma="scale")),
    ("tree", DecisionTreeClassifier(criterion='entropy', splitter="best", max_depth=5, random_state=42))
]

meta_model = LogisticRegression(C=1, class_weight="balanced", max_iter=1000)

stacked_model = StackingClassifier(estimators=base_model, final_estimator=meta_model, passthrough=True)
chi2_selector = SelectKBest(score_func=chi2, k=6)

process = Pipeline(steps=[
    ('preprocess', preprocessing),
    ('chi2', chi2_selector),
    ("model", stacked_model)
])

process.fit(X, y)
prediction = process.predict(X_test)
print(accuracy_score(y_test, prediction))
print(precision_score(y_test, prediction))
print(recall_score(y_test, prediction))
print(f1_score(y_test, prediction))
print(roc_auc_score(y_test, prediction))


# titanic_test = pd.read_csv("./test.csv")
# passenger_id = titanic_test["PassengerId"]
# titanic_test.drop(columns=["PassengerId", "Name", "Ticket"], inplace=True)

# survived_passengers = process.predict(titanic_test)

# new_titanic_data = pd.DataFrame(survived_passengers)
# new_titanic_data = pd.concat([passenger_id, new_titanic_data], axis=1)
# new_titanic_data.rename(columns={0: "Survived"}, inplace=True)
# new_titanic_data = new_titanic_data.to_csv("titan.csv", index=False)
    


