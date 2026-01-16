import sqlite3
import xml.etree.ElementTree as ET
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



def extract_goals_from_xml(goal_xml):
    """
    Parse the <goal> XML string and return a list of goal events.
    Handles matches with no goals (goal_xml=None).
    """
    goal_events = []
    
    if not goal_xml or pd.isna(goal_xml):
        return goal_events  # empty list if no goals
    
    root = ET.fromstring(goal_xml)
    
    for value in root.findall("value"):
        scorer = value.find("player1").text if value.find("player1") is not None else None
        assister = value.find("player2").text if value.find("player2") is not None else None
        team_id = value.find("team").text if value.find("team") is not None else None
        
        goal_events.append({
            "player_api_id": scorer,
            "team_api_id": team_id, 
            # "assister": assister,
        })
        
    return goal_events


def get_season_and_league():
    leagues = league_dataframe[["name"]].to_dict()["name"]
    season_options = input(f"Please select a season from the seasons: {match_dataframe["season"].unique().tolist()}: ")
    league_selection = int(input(f"Please select a league from the leagues: {league_dataframe[["name"]].to_dict()["name"]}: "))

    country_id = league_dataframe.loc[league_dataframe["name"] == leagues[league_selection]]["country_id"].iloc[0]

    matches_scored = match_dataframe.loc[(match_dataframe["season"] == season_options) &
                                         (match_dataframe["country_id"] == country_id)]
    
    matches_scored = match_dataframe.dropna(subset=["goal"])
    matches_scored["Goal Information"] = matches_scored["goal"].apply(extract_goals_from_xml)
    matches_scored = matches_scored.explode("Goal Information")

    return matches_scored


def get_scorer_from_series():

    matches_with_goals = get_season_and_league()
    goals_flat = pd.concat(
        [
            matches_with_goals.drop(columns=["Goal Information"]),
            matches_with_goals["Goal Information"].apply(pd.Series),
        ],
        axis=1
    )

    return goals_flat



def goal_derivation():

    player_team = get_scorer_from_series().groupby(["player_api_id", "team_api_id"]).size().reset_index(name="goals")
    player_team["player_api_id"] = player_team["player_api_id"].astype("int64")


    player_team = pd.merge(player_team, player_dataframe, on="player_api_id", how="left")
    player_team["team_api_id"] = player_team["team_api_id"].astype("int64")


    player_team = pd.merge(player_team, team_dataframe, on="team_api_id", how="left")
    player_team = player_team[["player_name", "team_long_name", "goals"]].sort_values(by="goals", ascending=False).head(30)


    return player_team


print(goal_derivation())