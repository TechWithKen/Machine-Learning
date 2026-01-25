import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, MaxAbsScaler
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
    salary_dataset = salary_dataset[['experience_level','job_title', 'company_location', "employment_type", "company_size"]]
    
    return {"salary_dataset": salary_dataset, "salary": salary}



def preprocess_data():
    X, y = get_salary()["salary_dataset"], get_salary()["salary"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    categorical_feature = ["experience_level", "employment_type"]
    ordinal_feature = [["S", "M", "L"]]
    column = ["company_size"]
    target_cols = ["job_title", "company_location"]



    preprocess = ColumnTransformer(transformers=[
                                                ("onehot", Pipeline(steps=[("encoder", OneHotEncoder(drop="first", sparse_output=False))]), categorical_feature),
                                                ('ord', Pipeline(steps=[("enconde_order", OrdinalEncoder(categories=ordinal_feature))]), column),
                                                ("tar", Pipeline(steps=[("encode_target", TargetEncoder())]), target_cols)
                                                ], remainder="passthrough")


    return {"X_train": X_train, "X_test": X_test, "y_train": y_train, "y_test": y_test, "preprocess": preprocess}



def model_training():
    preprocessed_data = preprocess_data()
    pipeline = Pipeline(steps=[
        ("preprocess", preprocessed_data["preprocess"]),
        ("model", LinearRegression()),
    ])


    pipeline.fit(preprocessed_data["X_train"], preprocessed_data["y_train"])

    prediction = pipeline.predict(preprocessed_data["X_test"])

    print(F"Predictions: - {prediction}\n")
    print(F"Accuracy = {pipeline.score(preprocessed_data["X_test"], preprocessed_data["y_test"]) * 100:.2f}% ")


model_training()
