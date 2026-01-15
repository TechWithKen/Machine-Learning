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
    home = create_outcome("home_team", {"H": "W", "A": "L", "D": "D"}, dataframe=premier_league_result)
    away = create_outcome("away_team", {"A": "W", "H": "L", "D": "D"}, dataframe=premier_league_result)


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
    
    team = dataframe[[f"{side_1}_team", f"{side_2}_goals"]] # for home team select away goal, for away team select home goals.
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


# You can edit the code from here to do other things, The dataframe itself is well formated to get the league table.

# Example Task - Analyze the goal difference of multiple teams across different seasons.
premier_league_results = pd.read_csv("./Laliga_results_csv")


def different_goal_difference(team1, team2):
    goal_difference_team1 = []
    goal_difference_team2 = []
    seasons = premier_league_results["season"].unique().tolist()

    visualizing_dataset = {"seasons": seasons, "team1": goal_difference_team1, "team2": goal_difference_team2}


    for season in seasons:
            global premier_league_result
            premier_league_result = premier_league_results.loc[premier_league_results["season"].str.contains(season)]

            premier_league_table = (get_premier_league_table(divide_home_away_team_results(), 
                            each_team_total_goals(), 
                            goal_conceded()))
            print(season)
            print(premier_league_table)
            
            goal_difference_team1.append(premier_league_table.loc[team1, "GF"].astype("int64"))
            goal_difference_team2.append(premier_league_table.loc[team2, "GF"].astype("int64"))

    return visualizing_dataset


seasons = premier_league_results["season"].unique().tolist()
for season in seasons:
        global premier_league_result
        premier_league_result = premier_league_results.loc[premier_league_results["season"].str.contains(season)]

        premier_league_table = (get_premier_league_table(divide_home_away_team_results(), 
                        each_team_total_goals(), 
                        goal_conceded()))
        print(season)
        print(premier_league_table)
# Visualizing a line graph for easy understanding of the analysis

# def plot_line_graph(first_team, second_team):
    

#     GD = different_goal_difference(first_team, second_team)
#     plt.figure(figsize=(12,6))
#     plt.plot(GD["seasons"], GD["team1"], marker='o', linestyle='-', color='red', label=first_team)
#     plt.plot(GD["seasons"], GD["team2"], marker='s', linestyle='--', color='blue', label=second_team)

#     plt.title("Goal Scored per Season")
#     plt.xlabel("Season")
#     plt.ylabel("Goal Difference (Goal Scored)")
#     plt.xticks(rotation=45)  # rotate season labels
#     plt.grid(True)
#     plt.legend()
#     plt.tight_layout()
#     plt.show()


# team1 = input("Please Enter the first team: ").title()
# team2 = input("Please Enter the second team: ").title()

# print(plot_line_graph(team1, team2))
