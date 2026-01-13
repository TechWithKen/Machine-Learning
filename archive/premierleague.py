import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def create_outcome(team_side, result_map, dataframe):
    team = dataframe[[team_side, "result"]]
    team["club"] = team[team_side]
    team["outcome"] = team["result"].map(result_map)
    team = team[["club", "outcome"]]

    return team

def divide_home_away_team_results():
    home = create_outcome("home_team", {"D": "Draw", "H": "Win", "A": "Loss"}, dataframe=premier_league_result)
    away = create_outcome("away_team", {"D": "Draw", "H": "Loss", "A": "Win"}, dataframe=premier_league_result)


    all_results = pd.concat([home, away], ignore_index=True)
    
    return all_results


def get_team_goals(team_side, side_goals, dataframe):
    team = dataframe[[team_side, side_goals]]
    team['club'] = team[team_side] 
    team["goals"] = team[side_goals]
    team = team[["club", "goals"]]

    return team


def each_team_total_goals():
    home = get_team_goals("home_team", "home_goals", dataframe=premier_league_result)
    away = get_team_goals("away_team", "away_goals", dataframe=premier_league_result)

    all_goals = pd.concat([home, away],ignore_index=True)
    total_goals = all_goals.pivot_table(index="club", values="goals", aggfunc="sum")

    return total_goals


def count_goals_conceded(side_1, side_2, dataframe):
    
    team = dataframe[[f"{side_1}_team", f"{side_2}_goals"]]
    team['club'] = team[f"{side_1}_team"]
    team["goals"] = team[f"{side_2}_goals"]
    team = team[["club", "goals"]]

    return team


def goal_conceded():

    home = count_goals_conceded("home", "away", dataframe=premier_league_result)

    away = count_goals_conceded("away", "home", dataframe=premier_league_result)

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


premier_league_results = pd.read_csv("results.csv")
premier_league_stat = pd.read_csv("stats.csv")


years = []
win_team = []
winners = {"Year": years, "Winner": win_team}

goal_difference_team1 = []
goal_difference_team2 = []
seasons = premier_league_results["season"].unique().tolist()
team1 = "Manchester United"
team2 = "Chelsea"

for season in seasons:
    premier_league_result = premier_league_results.loc[premier_league_results["season"].str.contains(season)]

    winning_team = (get_premier_league_table(divide_home_away_team_results(), 
                    each_team_total_goals(), 
                    goal_conceded()))
    print(season)
    print(winning_team)
    goal_difference_team1.append(winning_team.loc[team1, "GD"].astype("int64"))
    goal_difference_team2.append(winning_team.loc[team2, "GD"].astype("int64"))
#     years.append(season), win_team.append(winning_team.index[0])

# winning_dataframe = pd.DataFrame(winners)

# print(winning_dataframe)

 
# print(goal_difference)


# Plotting the graph

plt.figure(figsize=(12,6))
plt.plot(seasons, goal_difference_team1, marker='o', linestyle='-', color='red', label=team1)
plt.plot(seasons, goal_difference_team2, marker='s', linestyle='--', color='blue', label=team2)

plt.title("Goal Difference per Season")
plt.xlabel("Season")
plt.ylabel("Goal Difference (GD)")
plt.xticks(rotation=45)  # rotate season labels
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

