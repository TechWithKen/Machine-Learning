import pandas as pd
import numpy as np


premier_league_result = pd.read_csv("results.csv")
premier_league_stat = pd.read_csv("stats.csv")


premier_league_result = premier_league_result.loc[premier_league_result["season"].str.contains("2006-2007")]

def create_outcome(team_side, result_map):
    team = premier_league_result[[team_side, "result"]]
    team["club"] = team[team_side]
    team["outcome"] = team["result"].map(result_map)
    team = team[["club", "outcome"]]

    return team

def divide_home_away_team_results():
    home = create_outcome("home_team", {"D": "Draw", "H": "Win", "A": "Loss"})
    away = create_outcome("away_team", {"D": "Draw", "H": "Loss", "A": "Win"})


    all_results = pd.concat([home, away], ignore_index=True)
    
    return all_results


def get_team_goals(team_side, side_goals):
    team = premier_league_result[[team_side, side_goals]]
    team['club'] = team[team_side]
    team["goals"] = team[side_goals]
    team = team[["club", "goals"]]

    return team


def each_team_total_goals():
    home = get_team_goals("home_team", "home_goals")
    away = get_team_goals("away_team", "away_goals")

    all_goals = pd.concat([home, away],ignore_index=True)
    total_goals = all_goals.pivot_table(index="club", values="goals", aggfunc="sum")

    return total_goals


def count_goals_conceded(side_1, side_2):
    
    team = premier_league_result[[f"{side_1}_team", f"{side_2}_goals"]]
    team['club'] = team[f"{side_1}_team"]
    team["goals"] = team[f"{side_2}_goals"]
    team = team[["club", "goals"]]

    return team


def goal_conceded():

    home = count_goals_conceded("home", "away")

    away = count_goals_conceded("away", "home")

    all_goals = pd.concat([home, away],ignore_index=True)
    against_goals = all_goals.pivot_table(index="club", values="goals", aggfunc="sum")
    return against_goals


def get_premier_league_table(home_away_team, each_team_goals, goal_conceded):

    home_away_team_results = home_away_team.pivot_table(columns="outcome", index="club", aggfunc="size")
    played = home_away_team_results.sum(axis=1)
    home_away_team_results.insert(0, "P", played)
    home_away_team_results["PTS"] = (home_away_team_results["Draw"]*1) + (home_away_team_results["Win"]*3)

    league_table = home_away_team_results.merge(each_team_goals, on="club", how="inner")

    league_table = league_table.merge(goal_conceded, on="club", how="inner")
    league_table.rename(columns={"goals_x": "GF", "Draw": "D", "Loss": "L", "Win": "W", "goals_y": "GA"}, inplace=True)
    league_table["GD"] = league_table["GF"] - league_table["GA"]
    league_table = league_table.sort_values(by="PTS", ascending=False)


    remove_col = league_table.columns.tolist()
    remove_col.remove("PTS")
    remove_col.append("PTS")
    league_table = league_table[remove_col]
    league_table

    return league_table


print(get_premier_league_table(divide_home_away_team_results(), each_team_total_goals(), goal_conceded()))
