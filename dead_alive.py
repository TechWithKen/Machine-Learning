import pandas as pd
import numpy as np


# loading data
olympics_athlete = pd.read_parquet("olympicsParquet.parquet")

def living_athlete(filename):
    """Function to help get the dataframe of all living athlete"""
    living_athlete = filename.loc[filename["died_date"].isna()]
    living_athlete.drop(columns="died_date", inplace=True)
    living_athlete.dropna(subset=["born_date"], inplace=True)
    living_athlete["born_date"] = pd.to_datetime(living_athlete["born_date"])

    living_time = pd.Timestamp.today().normalize()

    living_athlete["Current Age"] = (living_time.year - living_athlete["born_date"].dt.year).astype("Int64")

    birthday_not_reached = (living_time.month < living_athlete["born_date"].dt.month) | (
        (living_time.month == living_athlete["born_date"].dt.month) & 
        (living_time.day < living_athlete["born_date"].dt.day) 
    )
    living_athlete.loc[birthday_not_reached, "Current Age"] = living_athlete["Current Age"] - 1

    return living_athlete.sort_values(by="Current Age", ascending=True).head(30)


def dead_athlete(filename):
    """Function to help get the dataframe of all dead athlete"""
    dead_athlete = filename.loc[~filename["died_date"].isna()]

    dead_athlete["born_date"] = pd.to_datetime(dead_athlete["born_date"])
    dead_athlete["died_date"] = pd.to_datetime(dead_athlete["died_date"])
    
    dead_athlete["Age of Death"] = (dead_athlete["died_date"].dt.year - dead_athlete["born_date"].dt.year).astype("Int64")

    birthday_not_reached = (dead_athlete["died_date"].dt.month < dead_athlete["born_date"].dt.month) | (
        (dead_athlete["died_date"].dt.month == dead_athlete["born_date"].dt.month) & 
        (dead_athlete["died_date"].dt.day < dead_athlete["born_date"].dt.day) 
    )

    dead_athlete.loc[birthday_not_reached, "Age of Death"] = dead_athlete["Age of Death"] - 1

    return dead_athlete.sort_values(by="Age of Death", ascending=True).head(30)


def athlete_record(sheet1, sheet2):

    with pd.ExcelWriter("Athlete_Records.xlsx", engine="openpyxl") as writer:
        sheet1.to_excel(writer, sheet_name="Living", index=False)
        sheet2.to_excel(writer, sheet_name="Dead", index=False)

    return "Created Successfully"


print(athlete_record(living_athlete(olympics_athlete), dead_athlete(olympics_athlete)))

