from weakref import finalize
from config import CSV_FILE, TEAM_CSV_FILE, PLAYER_TEAM_CSV_FILE, CITY_SCHEDULE, PLAYER_SCHEDULE, WEBHOOK
import pandas as pd
import random
import csv

def initialize_city_schedule(schedule_type):
    csv_name = ""
    if schedule_type == "city":
        csv_name = CITY_SCHEDULE
    else:
        csv_name = PLAYER_SCHEDULE

    #The season will be 12 weeks long, not every team will go against each other
    try:
        with open(CITY_SCHEDULE, "x", newline="") as file:
            writer = csv.writer(file)
            # Add headers to the CSV
            writer.writerow([prefix + str(i) for i in range(1, 13) for prefix in ("H", "A")])
    except FileExistsError:
        pass  # File already exists, no need to initialize


def create_schedule():
    initialize_city_schedule("city")
    initialize_city_schedule("player")

    city_teams = pd.read_csv(TEAM_CSV_FILE)
    city_teams = (city_teams["City"] + " " + city_teams["Team_Name"]).dropna().unique().tolist()

    player_teams = pd.read_csv(PLAYER_TEAM_CSV_FILE)
    player_teams = (player_teams["Owner"] + " " + player_teams["Team_Name"]).dropna().unique().tolist()

    city_schedule_df = generate_schedule_df(city_teams, allow_repeats=False)
    player_schedule_df = generate_schedule_df(player_teams, allow_repeats=True)

    city_schedule_df.to_csv(CITY_SCHEDULE, index=False)
    player_schedule_df.to_csv(PLAYER_SCHEDULE, index=False)


def generate_schedule_df(teams, allow_repeats):
    max_weeks = 12
    home_cols = [f"H{i}" for i in range(1, max_weeks + 1)]
    away_cols = [f"A{i}" for i in range(1, max_weeks + 1)]
    schedule = {col: [] for col in home_cols + away_cols}

    cycle_length = len(teams) // 2  # How many weeks before we reshuffle

    week_num = 1
    while week_num <= max_weeks:
        # Reshuffle every `cycle_length` weeks or at week 1
        if (week_num - 1) % cycle_length == 0 or week_num == 1:
            random.shuffle(teams)
            mid_index = len(teams) // 2
            list_1 = teams[:mid_index]  # Static list
            list_2 = teams[mid_index:]  # Rotating list

        # Rotate list_2 by 1
        list_2 = list_2[1:] + list_2[:1]  # Rotate left by 1

        week_matchups = []
        for i in range(len(list_1)):
            home = list_1[i]
            away = list_2[i]
            week_matchups.append((home, away))

        # Fill in the schedule for this week
        for home, away in week_matchups:
            schedule[f"H{week_num}"].append(home)
            schedule[f"A{week_num}"].append(away)

        # Fill up with BYEs if needed
        while len(schedule[f"H{week_num}"]) < len(teams) // 2:
            schedule[f"H{week_num}"].append("BYE")
            schedule[f"A{week_num}"].append("BYE")

        week_num += 1

    return pd.DataFrame(schedule)

def view_player_schedule(week_number=None):
    if week_number is None:
        try:
            week_number = int(input("Enter a week number to view the schedule: "))
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            return

    week_str = str(week_number)
    home_col = f"H{week_str}"
    away_col = f"A{week_str}"

    try:
        city_df = pd.read_csv(CITY_SCHEDULE)
        player_df = pd.read_csv(PLAYER_SCHEDULE)

        if home_col not in city_df.columns or away_col not in city_df.columns:
            print(f"Week {week_number} not found in the schedule.")
            return

        city_week = city_df[[home_col, away_col]].copy()
        player_week = player_df[[home_col, away_col]].copy()

        city_week.columns = ["City Home", "City Away"]
        player_week.columns = ["Player Home", "Player Away"]

        city_week.reset_index(drop=True, inplace=True)
        player_week.reset_index(drop=True, inplace=True)

        print(f"\n Week {week_number} City Matchups:\n")
        print(city_week)

        print(f"\n Week {week_number} Player Matchups:\n")
        print(player_week)

        return city_week, player_week

    except FileNotFoundError:
        print("One or both schedule files are missing!")
    except Exception as e:
        print(f"Unexpected error: {e}")

def finalize_week(week_number = None):
    from util import send_to_discord

    player_team_df = pd.read_csv(PLAYER_TEAM_CSV_FILE)
    players_df = pd.read_csv(CSV_FILE)

    try:
        week_number = int(input("Enter a week number to view the schedule: "))
    except ValueError:
        print("Invalid input. Please enter a valid number.")
        return

    week_str = str(week_number)
    home_col = f"H{week_str}"
    away_col = f"A{week_str}"
    print()


    send_to_discord(f"HEY GUYS! I HAVE THE NUMBERS FOR WEEK {week_number}", WEBHOOK)
    try:
        city_df = pd.read_csv(CITY_SCHEDULE)
        player_df = pd.read_csv(PLAYER_SCHEDULE)

        if home_col not in city_df.columns or away_col not in city_df.columns:
            print(f"Week {week_number} not found in the schedule.")
            return

        player_week = player_df[[home_col, away_col]].copy()

        player_week.columns = ["Player Home", "Player Away"]

        player_week.reset_index(drop=True, inplace=True)

        for idx, row in player_week.iterrows():
            home_team = row['Player Home']
            away_team = row["Player Away"]

            print(f"\n{home_team} vs {away_team}")
            team_one_active_players = []
            team_two_active_players = []

            # Get active players from the DataFrame, not from reading the CSV again
            for i, team_row in player_team_df.iterrows():
                full_team_name = f"{team_row['Owner']} {team_row['Team_Name']}"
                if full_team_name == home_team:
                    team_one_index = i
                    team_one_active_players = team_row[["QB1", "RB1", "RB2", "WR1", "WR2", "TE1", "FLEX", "K1", "DEF"]].tolist()
                elif full_team_name == away_team:
                    team_two_index = i
                    team_two_active_players = team_row[["QB1", "RB1", "RB2", "WR1", "WR2", "TE1", "FLEX", "K1", "DEF"]].tolist()

            team_one_score = players_df[players_df["Name"].isin(team_one_active_players)]["GPs"].sum()
            team_two_score = players_df[players_df["Name"].isin(team_two_active_players)]["GPs"].sum()

            print(f"{home_team}'s total score: {team_one_score}")
            print(f"{away_team}'s total score: {team_two_score}")

            # Update scores and records
            player_team_df.at[team_one_index, "scored_points"] += team_one_score
            player_team_df.at[team_two_index, "scored_points"] += team_two_score

            if team_one_score > team_two_score:
                send_to_discord(f"{home_team} beats {away_team}! Everyone point and laugh at {away_team}!", WEBHOOK)
                player_team_df.at[team_one_index, "wins"] += 1
                player_team_df.at[team_two_index, "losses"] += 1
            elif team_two_score > team_one_score:
                send_to_discord(f"{away_team} beats {home_team}! Everyone point and laugh at {home_team}!", WEBHOOK)
                player_team_df.at[team_two_index, "wins"] += 1
                player_team_df.at[team_one_index, "losses"] += 1
            else:
                send_to_discord(f"{home_team} and {away_team} Tie! Holy Shit I didn't think this would ever happen!", WEBHOOK)
                player_team_df.at[team_one_index, "ties"] += 1
                player_team_df.at[team_two_index, "ties"] += 1

            send_to_discord(f"{home_team}'s total score: {team_one_score}", WEBHOOK)
            send_to_discord(f"{away_team}'s total score: {team_two_score}", WEBHOOK)

        player_team_df.to_csv(PLAYER_TEAM_CSV_FILE, index=False)
        print("\nPlayer team data updated and saved.")

        # Reset GPs to 0 for all players
        players_df["GPs"] = 0
        players_df.to_csv(CSV_FILE, index=False)

    except FileNotFoundError:
        print("One or both schedule files are missing!")
    except Exception as e:
        print(f"Unexpected error: {e}")