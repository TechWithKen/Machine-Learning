import pandas as pd
import matplotlib.pyplot as plt

def create_outcome(team_side, result_map, dataframe):
    team = dataframe[[team_side, "result"]]
    team["club"] = team[team_side]
    team["outcome"] = team["result"].map(result_map)
    team = team[["club", "outcome"]]

    return team

def divide_home_away_team_results():

    # for home team H = Win, A = Loss
    # for the away team, H = Loss, A = Win
    home = create_outcome("home_team", {"H": "W", "A": "L", "D": "D"}, dataframe=league_result)
    away = create_outcome("away_team", {"A": "W", "H": "L", "D": "D"}, dataframe=league_result)


    all_results = pd.concat([home, away], ignore_index=True)
    
    return all_results


def get_team_goals(team_side, side_goals, dataframe):
    team = dataframe[[team_side, side_goals]]
    team['club'] = team[team_side] 
    team["goals"] = team[side_goals]
    team = team[["club", "goals"]]

    return team


def each_team_total_goals():
    home = get_team_goals("home_team", "home_goals", dataframe=league_result)
    away = get_team_goals("away_team", "away_goals", dataframe=league_result)

    all_goals = pd.concat([home, away],ignore_index=True)
    total_goals = all_goals.pivot_table(index="club", values="goals", aggfunc="sum")

    return total_goals


def count_goals_conceded(side_1, side_2, dataframe):
    
    team = dataframe[[f"{side_1}_team", f"{side_2}_goals"]] # for home team select away goal, for away team select home goals.
    team['club'] = team[f"{side_1}_team"]
    team["goals"] = team[f"{side_2}_goals"]
    team = team[["club", "goals"]]

    return team


def goal_conceded():

    home = count_goals_conceded("home", "away", dataframe=league_result)

    away = count_goals_conceded("away", "home", dataframe=league_result)

    all_goals = pd.concat([home, away],ignore_index=True)
    against_goals = all_goals.pivot_table(index="club", values="goals", aggfunc="sum")
    return against_goals


def get_league_table(home_away_team, each_team_goals, goal_conceded):

    home_away_team_results = home_away_team.pivot_table(columns="outcome", index="club", aggfunc="size")[["W", "D", "L"]] # Correct table order

    # Merge goals - (Goals Scored and Goals Conceeded)
    league_table = home_away_team_results.merge(each_team_goals, on="club", how="inner").merge(goal_conceded, on="club", how="inner")
    league_table.rename(columns={"goals_x": "GF", "goals_y": "GA"}, inplace=True) # goals_x = Goals Score, and goals_y = Goals Conceded
    league_table["GD"] = league_table["GF"] - league_table["GA"]
    league_table["PTS"] = (league_table["D"]*1) + (league_table["W"]*3)  # Win = +3 pts, Draw = +1 pts
    league_table = league_table.sort_values(by="PTS", ascending=False)
    played = home_away_team_results.sum(axis=1)
    league_table.insert(0, "P", played)


    return league_table

league_results = pd.read_csv("./7    Portugal Liga ZON Sagres_csv")
seasons = league_results["season"].unique().tolist()
for season in seasons:
        global league_result
        league_result = league_results.loc[league_results["season"].str.contains(season)]

        league_table = (get_league_table(divide_home_away_team_results(), 
                        each_team_total_goals(), 
                        goal_conceded()))
        print(season)
        print(league_table)
