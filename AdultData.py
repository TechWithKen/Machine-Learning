import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from category_encoders import TargetEncoder
from sklearn.impute import SimpleImputer
from sklearn.metrics import classification_report

cols_name = ["age", "workclass", "fnlwgt", "education", "education-num", "marital-status", "occupation", "relationship", "race", "sex", "capital-gain", "capital-loss", "hours-per-week", "native-country", "income"]

adult_dataset = pd.read_csv("./adult.data", names=cols_name)
adult_dataset["income"] = pd.get_dummies(adult_dataset["income"], drop_first=True, sparse=False)
fifty_k = adult_dataset["income"]

adult_dataset.drop(columns=["fnlwgt", "education", "income"], inplace=True)


categorical_features = ["workclass", "marital-status", "relationship", "race", "sex"]
num_features = ["age", "education-num", "capital-gain", "capital-loss", "hours-per-week"]
large_categorical_data = ["occupation", "native-country"]

## Data transformation and cleaning.

preprocessing = ColumnTransformer(transformers=[("cat", Pipeline(steps=[("impute", SimpleImputer(strategy="most_frequent")),
                                                                        ("encoder", OneHotEncoder(drop="first", sparse_output=False))]), categorical_features),
                                                ("num", Pipeline(steps=[("impute", SimpleImputer(strategy="mean")), ("scaler", StandardScaler())]), num_features),
                                                ("tar", Pipeline(steps=[("impute", SimpleImputer(strategy="most_frequent")), ("encoder", TargetEncoder())]),large_categorical_data)], remainder="passthrough")


pipeline = Pipeline(steps=[
    ("preprocess", preprocessing),
    ("model", LogisticRegression(max_iter=1000, class_weight="balanced"))
])

pipeline.fit(adult_dataset, fifty_k)

data_testing = pd.adult_dataset = pd.read_csv("./adult.test", names=cols_name)
data_testing["income"] = pd.get_dummies(data_testing["income"], drop_first=True, sparse=False)
data_testing_outcome = data_testing["income"]

data_testing.drop(columns=["fnlwgt", "education", "income"], inplace=True)
make_prediction = pipeline.predict(data_testing)

print(classification_report(make_prediction, data_testing_outcome))



