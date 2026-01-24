import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
from category_encoders import TargetEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline


def get_salary():

    salary_dataset = pd.read_csv("./ds_salaries.csv")
    salary_dataset = salary_dataset.drop_duplicates()
    salary = np.log1p(salary_dataset["salary_in_usd"]) #Convert the salary to logarithm, so the difference between a large and medium price won't be large.
    salary_dataset = salary_dataset[['experience_level','job_title', 'company_location', "employment_type", "remote_ratio", "company_size"]]
    
    return {"salary_dataset": salary_dataset, "salary": salary}



def preprocess_data():
    X, y = get_salary()["salary_dataset"], get_salary()["salary"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    categorical_feature = ["experience_level", "employment_type"]
    categorical_encoding = OneHotEncoder(drop="first", sparse_output=False)

    ordinal_feature = [["S", "M", "L"]]
    column = ["company_size"]
    ordinal_encoding = OrdinalEncoder(categories=ordinal_feature)

    target_cols = ["job_title", "company_location"]
    target = TargetEncoder(cols=target_cols)

    preprocess = ColumnTransformer(transformers=[("onehot", categorical_encoding, categorical_feature),
                                                ('ord', ordinal_encoding, column),
                                                ("tar", target, target_cols)], remainder="passthrough")


    return {"X_train": X_train, "X_test": X_test, "y_train": y_train, "y_test": y_test, "preprocess": preprocess}



def model_training():
    pipeline = Pipeline(steps=[
        ("preprocess", preprocess_data()["preprocess"]),
        ("model", LinearRegression()),
    ])


    pipeline.fit(preprocess_data()["X_train"], preprocess_data()["y_train"])

    prediction = pipeline.predict(preprocess_data()["X_test"])

    print(prediction)
    print(pipeline.score(preprocess_data()["X_test"], preprocess_data()["y_test"]))


model_training()
