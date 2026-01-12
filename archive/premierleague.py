import pandas as pd
import numpy as np


premier_league_result = pd.read_csv("results.csv")
premier_league_stat = pd.read_csv("stats.csv")


premier_league_result = premier_league_result.loc[premier_league_result["season"].str.contains("2015-2016")]


def divide_home_away_team_results():
    home = premier_league_result[["home_team", "result"]]
    home["club"] = home["home_team"]
    home["outcome"] = home["result"].map({
        "D": "Draw",
        "H": "Win",
        "A": "Loss"
    })
    home = home[["club", "outcome"]]


    away = premier_league_result[["away_team", "result"]]
    away["club"] = away["away_team"]
    away["outcome"] = away["result"].map({
        "D": "Draw",
        "H": "Loss",
        "A": "Win"
    })

    away = away[["club", "outcome"]]

    all_results = pd.concat([home, away], ignore_index=True)
    
    return all_results



def each_team_total_goals():
    home = premier_league_result[["home_team", "home_goals"]]
    home['club'] = home["home_team"]
    home["goals"] = home["home_goals"]
    home = home[["club", "goals"]]

    away = premier_league_result[["away_team", "away_goals"]]
    away["club"] = away["away_team"]
    away["goals"] = away["away_goals"]

    away = away[["club", "goals"]]

    all_goals = pd.concat([home, away],ignore_index=True)
    total_goals = all_goals.pivot_table(index="club", values="goals", aggfunc="sum")

    return total_goals


def goal_conceded():

    home = premier_league_result[["home_team", "away_goals"]]
    home['club'] = home["home_team"]
    home["goals"] = home["away_goals"]
    home = home[["club", "goals"]]

    away = premier_league_result[["away_team", "home_goals"]]
    away["club"] = away["away_team"]
    away["goals"] = away["home_goals"]
    away = away[["club", "goals"]]

    all_goals = pd.concat([home, away],ignore_index=True)
    against_goals = all_goals.pivot_table(index="club", values="goals", aggfunc="sum")
    return against_goals


def get_premier_league_table(home_away_team, each_team_goals, goal_conceded):

    home_away_team_results = home_away_team.pivot_table(columns="outcome", index="club", aggfunc="size")
    home_away_team_results["PTS"] = (home_away_team_results["Draw"]*1) + (home_away_team_results["Win"]*3)

    league_table = home_away_team_results.merge(each_team_goals, on="club", how="inner")
    league_table.insert(0, "P", 38)
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
