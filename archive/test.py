
#print(get_premier_league_table(divide_home_away_team_results(), each_team_total_goals(), goal_conceded()))
import pandas as pd 
import premierleague
global premier_league_result
premier_league_result = pd.read_csv("results.csv")
premier_league_stat = pd.read_csv("stats.csv")


#premier_league_result = premier_league_result.loc[premier_league_result["season"].str.contains("2006-2007")]
winners = {"Club": "Season"}

seasons = premier_league_result["season"].unique().tolist()

for season in seasons:
    premier_league_result = premier_league_result.loc[premier_league_result["season"].str.contains(season)]
    print(premierleague.get_premier_league_table(premierleague.divide_home_away_team_results(), 
                    premierleague.each_team_total_goals(), 
                    premierleague.goal_conceded()))

