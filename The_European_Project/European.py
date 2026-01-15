import sqlite3
import pandas as pd
import numpy as np

# Loading all data from the sql database

database_connection = sqlite3.connect("database.sqlite")
match_dataframe = pd.read_sql_query("SELECT * FROM Match", database_connection)
player_dataframe = pd.read_sql_query("SELECT * FROM Player", database_connection)
player_attributes_dataframe = pd.read_sql_query("SELECT * FROM Player_Attributes", database_connection)
league_dataframe = pd.read_sql_query("SELECT * FROM League", database_connection)
country_dataframe = pd.read_sql_query("SELECT * FROM Country", database_connection)
team_dataframe = pd.read_sql_query("SELECT * FROM Team", database_connection)
team_attributes_dataframe = pd.read_sql_query("SELECT * FROM Team_Attributes", database_connection)
sqlite_sequence = pd.read_sql_query("SELECT * FROM sqlite_sequence", database_connection)


# Filter the data and convert it to an to return just important data for each league table.
def generate_league_results_from_matches(country):

    country_league = pd.merge(country_dataframe, league_dataframe, on="id", how="inner")

    each_team = pd.merge(team_dataframe, team_attributes_dataframe, on="team_fifa_api_id", how="outer")
    each_team_data = each_team[["team_api_id_x", "team_long_name"]]

    matches_in_league = pd.merge(match_dataframe, country_league, on="country_id", how="inner")
    matches_in_league.rename(columns={"home_team_api_id":"team_api_id_x"}, inplace=True)


    home_team_league = pd.merge(matches_in_league, each_team_data, on="team_api_id_x", how="inner")

    league = home_team_league.loc[home_team_league["name_x"] == country]
    league.drop(columns=["team_api_id_x"], inplace=True)
    league.rename(columns={"away_team_api_id":"team_api_id_x", "team_long_name": "home_team"}, inplace=True)


    away_team = pd.merge(league, each_team_data, on="team_api_id_x", how="inner")
    league = away_team


    league.rename(columns={"team_long_name": "away_team"}, inplace=True)


    league["result"] = np.where(league["home_team_goal"] == league["away_team_goal"], "D", 
                                            (np.where(league["home_team_goal"] > league["away_team_goal"], "H", 
                                                        "A")))

    league = league[["home_team", "away_team", "home_team_goal", "away_team_goal", "result", "season"]].drop_duplicates()
    
    return {"league_results" : league, "league_name" : country_league}


# converting the dataframe to a csv file.
def generate_league_csv_data():

    country = input("Please enter the country you will like to check: ").title()
    league_data_dictionary = generate_league_results_from_matches(country)

    league_data_dictionary["league_results"].rename(columns={"home_team_goal": "home_goals", "away_team_goal":"away_goals"}, inplace=True)

    league_name = league_data_dictionary["league_name"].loc[(league_data_dictionary["league_name"])["name_x"] == country]["name_y"].to_string()

    league_data_dictionary["league_results"].to_csv(f"{league_name}_csv", index=False)

    return "League CSV Data Successfully created!"


print(generate_league_csv_data())