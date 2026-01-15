import pandas as pd
import matplotlib.pyplot as plt
import The_League_table


league_results = pd.read_csv("./premier_league_results_csv")
seasons = league_results["season"].unique().tolist()

def different_goal_difference(team1, team2):
    goal_difference_team1 = []
    goal_difference_team2 = []
    seasons = league_results["season"].unique().tolist()

    visualizing_dataset = {"seasons": seasons, "team1": goal_difference_team1, "team2": goal_difference_team2}


    for season in seasons:
            league_result = league_results.loc[league_results["season"].str.contains(season)]

            premier_league_table = (The_League_table.get_league_table(The_League_table.divide_home_away_team_results(league_result), 
                            The_League_table.each_team_total_goals(league_result), 
                            The_League_table.goal_conceded(league_result)))
            print(season)
            print(premier_league_table)
            
            goal_difference_team1.append(premier_league_table.loc[team1, "GF"].astype("int64"))
            goal_difference_team2.append(premier_league_table.loc[team2, "GF"].astype("int64"))

    return visualizing_dataset



# Visualizing a line graph for easy understanding of the analysis

def plot_line_graph(first_team, second_team):
    

    GD = different_goal_difference(first_team, second_team)
    plt.figure(figsize=(12,6))
    plt.plot(GD["seasons"], GD["team1"], marker='o', linestyle='-', color='red', label=first_team)
    plt.plot(GD["seasons"], GD["team2"], marker='s', linestyle='--', color='blue', label=second_team)

    plt.title("Goal Scored per Season")
    plt.xlabel("Season")
    plt.ylabel("Goal Difference (Goal Scored)")
    plt.xticks(rotation=45)  # rotate season labels
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


team1 = input("Please Enter the first team: ")
team2 = input("Please Enter the second team: ")



if __name__ == "__main__":
    print(plot_line_graph(team1, team2))
