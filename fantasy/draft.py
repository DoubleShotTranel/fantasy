import pandas as pd
import random
import csv
from config import CSV_FILE, TEAM_CSV_FILE, PLAYER_TEAM_CSV_FILE


def add_def_players():
    from fantasy import create_player
    try:
        players = []
        players_df = pd.read_csv(CSV_FILE)
        with open(TEAM_CSV_FILE, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                print(row)
                if row[0] == "City":
                    #skip the header
                    pass
                else:
                    players.append(create_player(auto_generate = False, position = "DEF", defense_name = f"{row[0]} {row[1]}"))
        with open(CSV_FILE, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(players)
        print("added stats to the teams defense")
    except FileNotFoundError:
        print("No teams found yet. Please create teams first.")

def city_draft():
    add_def_players()
    players_df = pd.read_csv(CSV_FILE)
    teams_df = pd.read_csv(TEAM_CSV_FILE)

    # Define draft order by position
    draft_positions = ["QB1", "QB2", "RB1", "RB2", "RB3", "RB4", "WR1", "WR2", "WR3", "WR4", "TE1", "TE2", "K1", "K2"]
    position_map = {"QB1": "QB", "QB2": "QB", "RB1": "RB", "RB2": "RB", "RB3": "RB", "RB4": "RB",
                    "WR1": "WR", "WR2": "WR", "WR3": "WR", "WR4": "WR", "TE1": "TE", "TE2": "TE",
                    "K1": "K", "K2": "K"}
    draft_order = teams_df.index.tolist()

    for round_num, position in enumerate(draft_positions):
        og_position = position
        position = position_map[position]
        draft_order = draft_order[3:] + draft_order[:3]  # Rotate by 3
        print(f"draft order: {draft_order}")

        for team_index in draft_order:
            
            team = teams_df.loc[team_index]
            team_name = team["Team_Name"]
            city_name = team["City"]

            # Find available players for the position (not yet drafted)
            available_players = players_df[
                (players_df["City_Team"] == "No Team") & 
                (players_df["Position"].str.upper() == position)
            ].sort_values(by="Projected_Skill", ascending=False)

            if not available_players.empty:
                # Select one of the 5 highest-rated available players
                selected_player = available_players.iloc[random.randint(0, 4)]
                player_name = selected_player["Name"]

                # Update player's City_Team field to match the team drafting them
                players_df.loc[players_df["Name"] == player_name, "City_Team"] = (f"{city_name} {team_name}")
                #update the status field
                if og_position in ["QB1", "RB1", "RB2", "WR1", "WR2", "TE1", "K1"]:
                    players_df.loc[players_df["Name"] == player_name, "Status"] = (f"Active")
                else:
                    players_df.loc[players_df["Name"] == player_name, "Status"] = (f"Benched")
                if pd.isna(teams_df.at[team_index, og_position]):  # Check if position is empty (NaN)
                    teams_df.at[team_index, og_position] = player_name  # Assign player to the team's position
                print(f"{city_name} {team_name} is Drafting {player_name}!")

    # Save updates to CSV
    players_df.to_csv(CSV_FILE, index=False)
    teams_df.to_csv(TEAM_CSV_FILE, index=False)
    
    print("Draft complete!")


def player_draft():
    from fantasy import view_player_teams, view_active_roster, check_position, check_bench, assign_player_to_team
    players_df = pd.read_csv(CSV_FILE)
    teams_df = pd.read_csv(PLAYER_TEAM_CSV_FILE)
    
    print(teams_df)
    #randomize draft order for first pick, then we'll make it a snake draft later
    og_draft_order = (teams_df.index.tolist())
    random.shuffle(og_draft_order)
    
    round_num = 1
    while round_num < 15:
        #snake draft logic
        if round_num % 2 == 0:
            draft_order = og_draft_order  # Normal order
        else:
            draft_order = og_draft_order[::-1]  # Reverse order
        draft_order_names = [f"{teams_df.loc[i, 'Owner']}" for i in draft_order]
        print(f"Draft order will be: {', '.join(draft_order_names)}. This draft will be a snake draft.")

        for team_index in draft_order:
            team = teams_df.iloc[team_index]
            team_name = team["Team_Name"]
            owner_name = team["Owner"]

            print(f"{owner_name}, you're up! Either type the name of who you want to draft or select an option!")
            done_with_turn = False
            
            while not done_with_turn:
                print()
                print("1: View Current Team")
                print("2: View Available Players")
                print("3: View All Active Players")
                print("4: Auto Draft")
                choice = input("Select an option: ").strip()
                if choice == "1":
                    view_player_teams(starting_df = teams_df[teams_df["Team_Name"] == team_name])
                elif choice == "2":
                    view_active_roster(starting_df = players_df, draft_filter=True)
                elif choice == "3":
                    view_active_roster(starting_df = players_df, draft_filter=False)
                elif choice == "4":
                    #AutoDraft
                    available_positions = players_df.loc[players_df["City_Team"] == "No Team", "Position"].unique().tolist()
                    available_positions.append("DEF")
                    valid_pos = False
                    while not valid_pos:
                        position = random.choice(available_positions)
                        print(f"maybe a {position}")
                        valid_pos = check_position(position = position, teams_df = teams_df, team_name = team_name)
                    print(f"The gods above have decided you need a {position}")

                    available_players = players_df[
                        (players_df["Player_Team"] == "No Team") & 
                        (players_df["Position"].str.upper() == position)
                    ].sort_values(by="Projected_Skill", ascending=False)

                    try:
                        selected_player = available_players.iloc[random.randint(0, 4)]
                    except:
                        selected_player = available_players.iloc[0]

                    choice = selected_player["Name"]
                    print(f"The gods have decided to draft {choice}")
                    players_df, teams_df = assign_player_to_team(players_df, teams_df, team_name, choice)
                    done_with_turn = True
                else:
                    #They are drafting a player or we have an invalid input
                    try:
                        players_df, teams_df = assign_player_to_team(players_df, teams_df, team_name, choice)
                        done_with_turn = True
                    except:
                        print(f"Invalid option, try again bozo \n (I know it was probably Jarrett's fault, but I was programmed to be rude)")

        round_num = round_num+1
    # Save updates to CSV
    players_df.to_csv(CSV_FILE, index=False)
    teams_df.to_csv(PLAYER_TEAM_CSV_FILE, index=False)
    
    print("Draft complete!")