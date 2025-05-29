from config import PLAYER_TEAM_CSV_FILE, CSV_FILE, TEAM_CSV_FILE
from tabulate import tabulate
import pandas as pd

def view_wl_record():
    teams_pd = pd.read_csv(PLAYER_TEAM_CSV_FILE)
    teams_pd = teams_pd[["Owner", "Team_Name", "wins", "losses", "ties", "scored_points"]].sort_values(by=["wins", "scored_points"], ascending=[False, False])
    print(tabulate(teams_pd, headers="keys", tablefmt="grid"))

def view_city_wl_record():
    teams_pd = pd.read_csv(TEAM_CSV_FILE)
    teams_pd = teams_pd[["City", "Team_Name", "wins", "losses"]].sort_values(by=["wins"], ascending=[False])
    print(tabulate(teams_pd, headers="keys", tablefmt="grid"))

def view_injury_report():
    players_pd = pd.read_csv(CSV_FILE)
    players_pd = players_pd[
        players_pd["Status"].isin(["Injured", "Dead"]) & (players_pd["Player_Team"] != "No Team")
    ]
    players_pd = players_pd[["Name", "Status", "Player_Team"]]
    print(tabulate(players_pd, headers="keys", tablefmt="grid"))

def check_for_nonsense():
    players_pd = pd.read_csv(CSV_FILE)
    players_pd = players_pd[
        players_pd["Status"].isin(["Benched"]) & (players_pd["City_Team"] == "No Team")
    ]
    players_pd = players_pd[["Name", "Status", "Position", "Player_Team"]]
    print(tabulate(players_pd, headers="keys", tablefmt="grid"))