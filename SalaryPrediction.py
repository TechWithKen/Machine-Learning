import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder
from category_encoders import TargetEncoder
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline

salary_dataset = pd.read_csv("./ds_salaries.csv")
salary_dataset = salary_dataset.drop_duplicates()
salary = np.log1p(salary_dataset["salary_in_usd"])

salary_dataset = salary_dataset[['experience_level','job_title', 'company_location', "employment_type", "remote_ratio", "company_size"]]

X, y = salary_dataset, salary

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

pipeline = Pipeline(steps=[
    ("preprocess", preprocess),
    ("model", LinearRegression()),
])


pipeline.fit(X_train, y_train)

prediction = pipeline.predict(X_test)

print(prediction)
print(pipeline.score(X_test, y_test))


## Model Accuracy, 59%

