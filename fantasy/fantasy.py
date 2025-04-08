from ast import List
import csv
import random
from tracemalloc import start
from turtle import position
import pandas as pd
from IPython.display import display
from tabulate import tabulate
import warnings
import time

from config import CSV_FILE, TEAM_CSV_FILE, PLAYER_TEAM_CSV_FILE, NAME_POOLS, POSITIONS, WEBHOOK
from Game_Sim import run_week, simulate_match
from draft import city_draft, player_draft
from scheduler import create_schedule, view_player_schedule
from team_manager import manage_team
from util import send_to_discord


# Function to generate a random name based on species
def generate_name(species):
    if species in NAME_POOLS:
        # Choose one from each category with an even distribution
        style = random.choice(["heroic", "villainous", "normal"])
        if style in ["normal"]:
            first_name = random.choice(NAME_POOLS[species]["first"])
            last_name = random.choice(NAME_POOLS[species]["last"]) 
        else:
            first_name = random.choice(NAME_POOLS[species]["wwe"])
            last_name = random.choice(NAME_POOLS[species][style])  # WWE-style last name for flair
        print(f"{first_name} {last_name} steps up to the challenge")
        return f"{first_name} {last_name}"
    else:
        # Default random name if species isn't in the list
        return f"{random.choice(NAME_POOLS['Fox']['heroic'])} {random.choice(NAME_POOLS['Fox']['wwe'])}"

# Function to get stat value (manual or random)
def get_stat(stat_name):
    choice = input(f"Enter {stat_name} (or type 'random' for a value between 1 and 100): ").strip().lower()
    if choice == "random":
        return random.randint(1, 100)
    try:
        value = int(choice)
        if 1 <= value <= 100:
            return value
        else:
            print("Value must be between 1 and 100. Assigning a random value.")
    except ValueError:
        rand_num = random.randint(1, 100)
        print(f"Invalid input. Assigning a random value: {rand_num}")
    return random.randint(1, 100)

def get_position(auto_generate=False):
    if not auto_generate:
        print(f"Potential positions: {POSITIONS}")
        choice = input(f"Enter position (or type 'random' for a random position): ").strip().lower()
        if choice in POSITIONS:
            return choice
    return random.choice(POSITIONS)

# Function to create a player
def create_player(auto_generate = False, position = "", defense_name = ""):
    if auto_generate:
        species = random.choice(list(NAME_POOLS.keys()))
        name = generate_name(species)
        speed = random.randint(1, 100)
        strength = random.randint(1, 100)
        gumption = random.randint(1, 100)
        finesse = random.randint(1, 100)
        accuracy = random.randint(1, 100)
        wow_factor = random.randint(1, 100)
        position = get_position(auto_generate)
        status = "Healthy"
        city_team = "No Team"
        player_team = "No Team"
        #Different positions care about different traits, so an accurate projected score also cares about position
        projected_skill = 0
        if position == ("QB"):
            projected_skill = int((strength*0.8 + gumption*1.2 + finesse*0.8 + accuracy*1.5 + speed*0.7)/5)
        elif position == ("RB"):
            projected_skill = int((gumption*1.2 + finesse*1.2 + wow_factor*0.6)/3)
        elif position == ("WR"):
            projected_skill = int((speed*1.2 + finesse*1.2 + wow_factor*0.6)/3)
        elif position == ("TE"):
            projected_skill = int((gumption*1.2 + finesse*1.2 + wow_factor*0.6)/3)
        elif position == ("K"):
            projected_skill = int(accuracy * 0.75) #The kickers aren't that great calm down
        else:
            projected_skill = int((speed+strength+gumption+finesse+accuracy+wow_factor)/6)
        catchphrase = input("Enter catchphrase: ") if not auto_generate else f"{name} is ready to roll!"
    else:
        if position == "":
            species = input(f"Enter species {list(NAME_POOLS.keys())}: ").strip()
            species_list = [species_name.lower for species_name in list(NAME_POOLS.keys())]
            if species not in NAME_POOLS:
                print("Unknown species. Assigning a random one.")
                species = random.choice(list(NAME_POOLS.keys()))
                print(f"Your species is {species}")
            name = input("Enter name (or type 'random' for an auto-generated name): ").strip()
            if name.lower() == "random" or name.lower() == "":
                name = generate_name(species)

            speed = get_stat("Speed")
            strength = get_stat("Strength")
            gumption = get_stat("Gumption")
            finesse = get_stat("Finesse")
            accuracy = get_stat("Accuracy")
            wow_factor = get_stat("Wow Factor")
            position = get_position(auto_generate)
            status = "Healthy"
            city_team = "No Team"
            player_team = "No Team"

            #Different positions care about different traits, so an accurate projected score also cares about position
            projected_skill = 0
            if position == ("QB"):
                projected_skill = int((strength*0.8 + gumption*1.2 + finesse*0.8 + accuracy*1.5 + speed*0.7)/5)
            elif position == ("RB"):
                projected_skill = int((gumption*1.2 + finesse*1.2 + wow_factor*0.6)/3)
            elif position == ("WR"):
                projected_skill = int((speed*1.2 + finesse*1.2 + wow_factor*0.6)/3)
            elif position == ("TE"):
                projected_skill = int((gumption*1.2 + finesse*1.2 + wow_factor*0.6)/3)
            elif position == ("K"):
                projected_skill = int(accuracy * 0.75) #The kickers aren't that great calm down
            else:
                projected_skill = int((speed+strength+gumption+finesse+accuracy+wow_factor)/6)
            catchphrase = input("Enter catchphrase: ") if not auto_generate else f"{name} is ready to roll!"

            print(f"Profesionals project {name} to be at a {projected_skill} skill level!")
            if projected_skill < 6:
                print("Jesus Christ how is this thing even alive?")
            elif projected_skill < 33:
                print("Wow! That's real bad!")
            elif projected_skill < 50:
                print("This is a risky pick!")
            elif projected_skill < 66:
                print("Not too shabby!")
            elif projected_skill < 95:
                print(f"This is a {species} I wouldn't mind having on my team!")
            else:
                print("What a legend!")
            print()
    
        #we're adding a defense
        else:
            projected_skill = int((random.randint(1, 100)+random.randint(1, 100)+random.randint(1, 100)+random.randint(1, 100)+random.randint(1, 100))/5)
            if projected_skill < 55:
                projected_skill = projected_skill + 20
            return [f"{defense_name} Defense", "DEF", "",0,0,0,0,0,0,"",projected_skill,"Active","No Team",defense_name, 0, 0]
    return [name, position, species, speed, strength, gumption, finesse, accuracy, wow_factor, catchphrase, projected_skill, status, player_team, city_team, 0, 0]

# Function to add a single or multiple players
def add_players():
    initialize_csv()
    players = []
    players_df = pd.read_csv(CSV_FILE)
    bulk = input("Would you like to add multiple players? (yes/no): ").strip().lower()

    if bulk == "yes":
        num_players = input("How many players do you want to add? ")
        try:
            num_players = int(num_players)
            auto_generate = input("Do you want to auto-generate names and species? (yes/no): ").strip().lower() == "yes"
        
            # Check for existing players to prevent duplicates
            existing_players = players_df["Name"].tolist()  # Assuming 'players_df' holds your player data
        
            for _ in range(num_players):
                # Create the player (returns a pandas Series or dict)
                new_player = create_player(auto_generate=auto_generate, position="")
            
                new_player_name = new_player[0]
            
                if new_player_name and new_player_name not in existing_players:
                    players.append(new_player)
                    # Also, add the new player to existing_players list to prevent further duplicates in this bulk add
                    existing_players.append(new_player_name)
                else:
                    print(f"Player {new_player_name} already exists. Skipping.")
        except ValueError:
            print("Invalid number. Exiting.")
            return


    else:
        players.append(create_player())

    with open(CSV_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(players)

    print(f"{len(players)} player(s) have been added to the roster!")

#These will be the teams real people manage
def add_player_team():
    initialize_player_team_csv()
    owner = input("Enter team owner's name: ").strip()
    name = input("Enter the name of the team: ").strip()

    # Initialize the positions to blank
    positions = {
        "QB1": "",
        "RB1": "",
        "RB2": "",
        "WR1": "",
        "WR2": "",
        "TE1": "",
        "FLEX": "",
        "K1": "",
        "DEF": "",
        "Bench1": "",
        "Bench2": "",
        "Bench3": "",
        "Bench4": "",
        "Bench5": "",
        "wins": 0,
        "losses": 0,
        "ties": 0,
        "scored_points": 0
    }

    # Prepare the team data
    team_data = [owner, name] + list(positions.values())
    
    # Save the PLAYER_TEAM_CSV_FILE to the CSV
    with open(PLAYER_TEAM_CSV_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(team_data)
    
    print(f"Team '{name}' managed by {owner} has been created!")

# Function to create a team
def create_team():
    initialize_team_csv()
    # Get team information from the user
    city = input("Enter the city for the team: ").strip()
    name = input("Enter the team name: ").strip()
    
    # Initialize the positions to blank
    positions = {
        "QB1": "",
        "QB2": "",
        "RB1": "",
        "RB2": "",
        "RB3": "",
        "RB4": "",
        "WR1": "",
        "WR2": "",
        "WR3": "",
        "WR4": "",
        "TE1": "",
        "TE2": "",
        "K1": "",
        "K2": "",
        "wins": 0,
        "losses": 0
    }
    
    # Prepare the team data
    team_data = [city, name] + list(positions.values())
    
    # Save the team to the CSV
    with open(TEAM_CSV_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(team_data)
    
    print(f"Team '{name}' from {city} has been created!")

# Function to view the teams
def view_teams(starting_df = None):
    try:
        with open(TEAM_CSV_FILE, "r") as file:
            reader = csv.reader(file)
            #next(reader)  # Skip the header row
            print("\n--- Current Teams ---")
            for row in reader:
                print(f"Team: {row[0]} {row[1]}")
                print("Starters:")
                print(f"     QB:{row[2]}")
                print(f"     RB:{row[4]}")
                print(f"     RB:{row[5]}")
                print(f"     WR:{row[8]}")
                print(f"     WR:{row[9]}")
                print(f"     TE:{row[12]}")
                print(f"     K:{row[14]}")
                print("Bench:")
                print(f"     {row[3]},  {row[6]},  {row[7]},  {row[10]},  {row[11]},  {row[13]},  {row[15]},")
                print()
    except FileNotFoundError:
        print("No teams found yet. Please create teams first.")

# Function to view the player owned teams
def view_player_teams(starting_df = None):
    try:
        if not starting_df.empty:
            df = starting_df
            team_data = df[["Team_Name", "Owner"]]
            big_dogs = df[["QB1", "FLEX"]]
            rb = df[["RB1", "RB2"]]
            wr = df[["WR1", "WR2"]]
            misc = df[["TE1", "K1", "DEF"]]
            bench = df[["Bench1", "Bench2", "Bench3", "Bench4", "Bench5"]]

            # Print the formatted table
            print(tabulate(team_data, headers="keys", tablefmt="grid"))
            print(tabulate(big_dogs, headers="keys", tablefmt="grid"))
            print(tabulate(rb, headers="keys", tablefmt="grid"))
            print(tabulate(wr, headers="keys", tablefmt="grid"))
            print(tabulate(misc, headers="keys", tablefmt="grid"))
            print(tabulate(bench, headers="keys", tablefmt="grid"))
    except:
        try:
            with open(PLAYER_TEAM_CSV_FILE, "r") as file:
                reader = csv.reader(file)
                #next(reader)  # Skip the header row
                print("\n--- Current Teams ---")
                for row in reader:
                    print(f"Team: {row[0]} {row[1]}")
                    print("Starters:")
                    print(f"     QB:{row[2]}")
                    print(f"     RB:{row[3]}")
                    print(f"     RB:{row[4]}")
                    print(f"     WR:{row[5]}")
                    print(f"     WR:{row[6]}")
                    print(f"     TE:{row[7]}")
                    print(f"     FLEX:{row[8]}")
                    print(f"     K:{row[9]}")
                    print(f"     DEF:{row[10]}")
                    print("Bench:")
                    print(f"     {row[11]},  {row[12]},  {row[13]},  {row[14]},  {row[15]},")
                    print()
        except FileNotFoundError:
            print("No teams found yet. Please create teams first.")

# Player CSV
def initialize_csv():
    try:
        with open(CSV_FILE, "x", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Position", "Species", "Speed", "Strength", "Gumption", "Finesse", "Accuracy", "Wow_Factor", 
                             "Catchphrase", "Projected_Skill", "Status", "Player_Team", "City_Team", "GPs", "TPs"])
    except FileExistsError:
        pass  # File already exists, no need to initialize

# Function to initialize the CSV file with headers
def initialize_team_csv():
    try:
        with open(TEAM_CSV_FILE, "x", newline="") as file:
            writer = csv.writer(file)
            # Add headers to the CSV
            writer.writerow(["City", "Team_Name", 
                             "QB1", "QB2", "RB1", "RB2", "RB3", "RB4", "WR1", "WR2", "WR3", "WR4", "TE1", "TE2", "K1", "K2",
                             "wins","losses"])
    except FileExistsError:
        pass  # File already exists, no need to initialize

# Function to initialize the CSV file with headers
def initialize_player_team_csv():
    try:
        with open(PLAYER_TEAM_CSV_FILE, "x", newline="") as file:
            writer = csv.writer(file)
            # Add headers to the CSV
            writer.writerow(["Owner", "Team_Name",
                            "QB1", "RB1", "RB2", "WR1", "WR2", "TE1", "FLEX", "K1", "DEF",
                            "Bench1", "Bench2", "Bench3", "Bench4", "Bench5",
                            "wins", "losses", "ties","scored_points"])
    except FileExistsError:
        pass  # File already exists, no need to initialize

def view_roster(position=None):
    try:
        df = pd.read_csv(CSV_FILE)  # Load the CSV into a DataFrame

        if df.empty:
            print("No roster found yet. Please add players first.")
            return

        # Ensure column names are consistent
        df.columns = df.columns.str.strip()  # Remove any accidental spaces

        position = input("Enter a position to filter by (QB/RB/WR/TE/K/DEF or press Enter to view all): ").strip()

        # Filter by position if specified
        if position:
            df = df[df["Position"].str.upper() == position.upper()]  # Proper filtering

        # Select only the desired columns
        display_df = df[["Name", "Position", "Species", "Projected_Skill", "City_Team", "Player_Team", "Status"]]

        # Sort by highest projected score
        display_df = display_df.sort_values(by="Projected_Skill", ascending=False)

        # Print the formatted table
        print(tabulate(display_df, headers="keys", tablefmt="grid"))

    except FileNotFoundError:
        print("No roster found yet. Please add players first.")
    except KeyError as e:
        print(f"Missing expected column in CSV: {e}")

def view_active_roster(position=None, starting_df = None, draft_filter = False):
    has_df = False
    try:
        if not starting_df.empty:
            df = starting_df
            has_df = True
            active_filter = "yes"
        else:
            df = pd.read_csv(CSV_FILE)  # Load the CSV into a DataFrame

            if df.empty:
                print("No roster found yet. Please add players first.")
                return
    except:
        # Ensure column names are consistent
        if not has_df:
            df = pd.read_csv(CSV_FILE)
            active_filter = input("Do you want to filter out the benched player?: ").strip()

    df.columns = df.columns.str.strip()  # Remove any accidental spaces

    position = input("Enter a position to filter by (QB/RB/WR/TE/K/DEF or press Enter to view all): ").strip()
    if draft_filter:
        df = df[df["Status"].str.upper() == "ACTIVE"]
        df = df[df["Player_Team"] == "No Team"]
    else:
        
        if active_filter == "yes":
            df = df[df["Status"].str.upper() == "ACTIVE"]
        else:
            df = df[df["Status"].str.upper().isin(["ACTIVE", "BENCHED"])]
        

    # Filter by position if specified
    if position:
        df = df[df["Position"].str.upper() == position.upper()]  # Proper filtering
        

    # Select only the desired columns
    display_df = df[["Name", "Position", "Species", "Projected_Skill", "City_Team", "Player_Team", "Status", "GPs", "TPs"]]

    # Sort by highest projected score
    display_df = display_df.sort_values(by=["TPs", "Projected_Skill"], ascending=[False, False])    

    # Print the formatted table
    print(tabulate(display_df, headers="keys", tablefmt="grid"))

def view_player_matchup(team_one = None, team_two = None):
    team_one_active_players = []
    team_two_active_players = []

    players_df = pd.read_csv(CSV_FILE)

    try:
        if(team_one == None or team_two == None):
            team_one_owner = input("Team 1 Owner: ")
            team_two_owner = input("Team 2 Owner: ")

        with open(PLAYER_TEAM_CSV_FILE, "r") as file:
            reader = csv.reader(file)
            #next(reader)  # Skip the header row
            print("\n--- Current Teams ---")
            for row in reader:
                if row[0] == team_one_owner:
                    team_one_active_players.append(row[2]) #QB
                    team_one_active_players.append(row[3]) #RB
                    team_one_active_players.append(row[4]) #RB
                    team_one_active_players.append(row[5]) #WR
                    team_one_active_players.append(row[6]) #WR
                    team_one_active_players.append(row[7]) #TE
                    team_one_active_players.append(row[8]) #FLEX
                    team_one_active_players.append(row[9]) #K
                    team_one_active_players.append(row[10]) #DEF
                elif row[0] == team_two_owner:
                    team_two_active_players.append(row[2]) #QB
                    team_two_active_players.append(row[3]) #RB
                    team_two_active_players.append(row[4]) #RB
                    team_two_active_players.append(row[5]) #WR
                    team_two_active_players.append(row[6]) #WR
                    team_two_active_players.append(row[7]) #TE
                    team_two_active_players.append(row[8]) #FLEX
                    team_two_active_players.append(row[9]) #K
                    team_two_active_players.append(row[10]) #DEF

        position_order = ['QB', 'RB', 'WR', 'TE', 'K', 'DEF']

        # Filter down a copy of the dataset to the relevant fields of the coach 1 team
        team_one_players = players_df.loc[
            players_df['Name'].isin(team_one_active_players),
            ['Name', 'Position', 'Player_Team', 'City_Team', 'GPs']
        ].copy()

        team_one_players['Position'] = pd.Categorical(
            team_one_players['Position'],
            categories=position_order,
            ordered=True
        )

        team_one_players = team_one_players.sort_values('Position')

        # Filter down a copy of the dataset to the relevant fields of the coach 2 team
        team_two_players = players_df.loc[
            players_df['Name'].isin(team_two_active_players),
            ['Name', 'Position', 'Player_Team', 'City_Team', 'GPs']
        ].copy()

        team_two_players['Position'] = pd.Categorical(
            team_two_players['Position'],
            categories=position_order,
            ordered=True
        )

        team_two_players = team_two_players.sort_values('Position')

        print(tabulate(team_one_players, headers="keys", tablefmt="grid"))
        print(tabulate(team_two_players, headers="keys", tablefmt="grid"))

        # Calculate and print team scores
        team_one_score = team_one_players['GPs'].sum()
        team_two_score = team_two_players['GPs'].sum()
        print(f"{team_one_owner}'s total score: {team_one_score} \n{team_two_owner}'s total score: {team_two_score}")

    except Exception as ex:
        print(ex)

        print("Invalid team name, try again")
        view_player_matchup(team_one = None, team_two = None)

def add_def_players():
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

def assign_player_to_team(players_df, teams_df, team_name, choice):
    #set the players team to the current person drafting
    player_assigned = False
                        
    if(players_df.loc[players_df["Name"] == choice, "Player_Team"].values[0] != "No Team"):
        print(f"player already belongs to {players_df.loc[players_df['Name'] == choice, 'Player_Team'].values[0]}")
        print("Stealing isn't nice")
    else:
        players_df.loc[players_df["Name"] == choice, "Player_Team"] = (f"{team_name}")
        pos_to_draft = players_df.loc[players_df["Name"] == choice, "Position"].values[0]

        print(pos_to_draft)
        if(pos_to_draft == "QB"):
            if str(teams_df.loc[teams_df["Team_Name"] == team_name, "QB1"].values[0]) == "nan":
                teams_df.loc[teams_df["Team_Name"] == team_name, "QB1"] = choice
                player_assigned = True
        elif pos_to_draft == "WR":
            #WR1
            if str(teams_df.loc[teams_df["Team_Name"] == team_name, "WR1"].values[0]) == "nan":
                teams_df.loc[teams_df["Team_Name"] == team_name, "WR1"] = choice
                player_assigned = True

            #WR2
            elif str(teams_df.loc[teams_df["Team_Name"] == team_name, "WR2"].values[0]) == "nan":
                teams_df.loc[teams_df["Team_Name"] == team_name, "WR2"] = choice
                player_assigned = True

            #FLEX
            elif str(teams_df.loc[teams_df["Team_Name"] == team_name, "FLEX"].values[0]) == "nan":
                teams_df.loc[teams_df["Team_Name"] == team_name, "FLEX"] = choice
                player_assigned = True
        elif pos_to_draft == "RB":
            #RB1
            if str(teams_df.loc[teams_df["Team_Name"] == team_name, "RB1"].values[0]) == "nan":
                teams_df.loc[teams_df["Team_Name"] == team_name, "RB1"] = choice
                player_assigned = True

            #RB2
            elif str(teams_df.loc[teams_df["Team_Name"] == team_name, "RB2"].values[0]) == "nan":
                teams_df.loc[teams_df["Team_Name"] == team_name, "RB2"] = choice
                player_assigned = True

            #FLEX
            elif str(teams_df.loc[teams_df["Team_Name"] == team_name, "FLEX"].values[0]) == "nan":
                teams_df.loc[teams_df["Team_Name"] == team_name, "FLEX"] = choice
                player_assigned = True
        elif pos_to_draft == "TE":
            if str(teams_df.loc[teams_df["Team_Name"] == team_name, "TE1"].values[0]) == "nan":
                teams_df.loc[teams_df["Team_Name"] == team_name, "TE1"] = choice
                player_assigned = True

            #FLEX
            elif str(teams_df.loc[teams_df["Team_Name"] == team_name, "FLEX"].values[0]) == "nan":
                teams_df.loc[teams_df["Team_Name"] == team_name, "FLEX"] = choice
                player_assigned = True
        elif pos_to_draft == "K":
            if str(teams_df.loc[teams_df["Team_Name"] == team_name, "K1"].values[0]) == "nan":
                teams_df.loc[teams_df["Team_Name"] == team_name, "K1"] = choice
                player_assigned = True
        elif pos_to_draft == "DEF":
            if str(teams_df.loc[teams_df["Team_Name"] == team_name, "DEF"].values[0]) == "nan":
                teams_df.loc[teams_df["Team_Name"] == team_name, "DEF"] = choice
                player_assigned = True
        else:
            print("What the fuck")


        if not player_assigned: #assign the player to the bench
            if str(teams_df.loc[teams_df["Team_Name"] == team_name, "Bench1"].values[0]) == "nan":
                teams_df.loc[teams_df["Team_Name"] == team_name, "Bench1"] = choice
            elif str(teams_df.loc[teams_df["Team_Name"] == team_name, "Bench2"].values[0]) == "nan":
                teams_df.loc[teams_df["Team_Name"] == team_name, "Bench2"] = choice
            elif str(teams_df.loc[teams_df["Team_Name"] == team_name, "Bench3"].values[0]) == "nan":
                teams_df.loc[teams_df["Team_Name"] == team_name, "Bench3"] = choice
            elif str(teams_df.loc[teams_df["Team_Name"] == team_name, "Bench4"].values[0]) == "nan":
                teams_df.loc[teams_df["Team_Name"] == team_name, "Bench4"] = choice
            elif str(teams_df.loc[teams_df["Team_Name"] == team_name, "Bench5"].values[0]) == "nan":
                teams_df.loc[teams_df["Team_Name"] == team_name, "Bench5"] = choice

            player_assigned = True
        
    return players_df, teams_df

def check_bench(teams_df, team_name):
    if str(teams_df.loc[teams_df["Team_Name"] == team_name, "Bench1"].values[0]) == "nan":
        return True
    elif str(teams_df.loc[teams_df["Team_Name"] == team_name, "Bench2"].values[0]) == "nan":
        return True
    elif str(teams_df.loc[teams_df["Team_Name"] == team_name, "Bench3"].values[0]) == "nan":
        return True
    elif str(teams_df.loc[teams_df["Team_Name"] == team_name, "Bench4"].values[0]) == "nan":
        return True
    elif str(teams_df.loc[teams_df["Team_Name"] == team_name, "Bench5"].values[0]) == "nan":
        return True
    return False

def check_position(position, teams_df, team_name):
    if position == "QB":
        if str(teams_df.loc[teams_df["Team_Name"] == team_name, "QB1"].values[0]) == "nan":
            return True

    if position == "WR":
        if str(teams_df.loc[teams_df["Team_Name"] == team_name, "WR1"].values[0]) == "nan":
            return True
        if str(teams_df.loc[teams_df["Team_Name"] == team_name, "WR2"].values[0]) == "nan":
            return True
        if str(teams_df.loc[teams_df["Team_Name"] == team_name, "FLEX"].values[0]) == "nan":
            return True

    if position == "RB":
        if str(teams_df.loc[teams_df["Team_Name"] == team_name, "RB1"].values[0]) == "nan":
            return True
        if str(teams_df.loc[teams_df["Team_Name"] == team_name, "RB2"].values[0]) == "nan":
            return True
        if str(teams_df.loc[teams_df["Team_Name"] == team_name, "FLEX"].values[0]) == "nan":
            return True

    if position == "TE":
        if str(teams_df.loc[teams_df["Team_Name"] == team_name, "TE1"].values[0]) == "nan":
            return True
        if str(teams_df.loc[teams_df["Team_Name"] == team_name, "FLEX"].values[0]) == "nan":
            return True

    if position == "K":
        if str(teams_df.loc[teams_df["Team_Name"] == team_name, "K1"].values[0]) == "nan":
            return True

    if position == "DEF":
        if str(teams_df.loc[teams_df["Team_Name"] == team_name, "DEF"].values[0]) == "nan":
            return True

    return(check_bench(teams_df, team_name))

def get_player_by_pos(position, team_name, players_df):
    get_all = players_df[players_df["City_Team"] == team_name]
    get_all = get_all[get_all["Status"] == "Active"]
    player = get_all[players_df["Position"] == position]
    return player

def get_team_df(team_name, teams_df):
    return teams_df[teams_df["Team_Name"] == team_name]

def get_defense_skill(players_df, team_name):
    get_all = players_df[players_df["City_Team"] == team_name]
    def_df = get_all[players_df["Position"] == "DEF"]["Projected_Skill"].values[0]
    print(f"def skill: {def_df}")
    return(def_df)

def update_team_points(winning_team, losing_team, team_type=None):
    if team_type == "City Team":
        df_to_update = pd.read_csv(TEAM_CSV_FILE)
    else:
        df_to_update = pd.read_csv(PLAYER_TEAM_CSV_FILE)
    print(winning_team)

    # Ensure columns exist before updating
    if 'Team_Name' in df_to_update.columns and 'wins' in df_to_update.columns and 'losses' in df_to_update.columns:
        # Update wins for the winning team
        if team_type == "City Team":
            df_to_update.loc[df_to_update['City'] + " " + df_to_update['Team_Name'] == winning_team, 'wins'] += 1

            # Update losses for the losing team
            df_to_update.loc[df_to_update['City'] + " " + df_to_update['Team_Name'] == losing_team, 'losses'] += 1

        # Save the updated DataFrame back to the CSV
        if team_type == "City Team":
            df_to_update.to_csv(TEAM_CSV_FILE, index=False)
        else:
            df_to_update.to_csv(PLAYER_TEAM_CSV_FILE, index=False)
    else:
        print("Expected columns 'Team_Name', 'wins', or 'losses' not found in the CSV.")

def reset_GPs(reset_TPs = False):
    players_df = pd.read_csv(CSV_FILE)

    #reset scores after game
    players_df['GPs'] = 0

    # This will only really be done for debugging
    if reset_TPs:
        confirm = input("Are you sure you want to reset TPs? ")
        if confirm == "yes":
            players_df['TPs'] = 0

    # Save the modified DataFrame back to the CSV file
    players_df.to_csv(CSV_FILE, index=False)
    print("reset game scores")


if __name__ == "__main__":
    warnings.simplefilter(action='ignore', category=FutureWarning)
    warnings.simplefilter(action='ignore', category=UserWarning)
    send_to_discord("hey", WEBHOOK)
    while True:
        print("\n--- Player Roster Management ---")
        print("1. Add Players")
        print("2. View City Teams")
        print("3. View Active Roster")
        print("4. Create Player Team")
        print("5. View Player Teams")
        print("6. Player Draft")
        print("7. View Player Matchup")
        print("8. View Week Matchups")
        print("9. Manage Team")

        #secret options for Jarrett
        #99 = create defenses for city teams
        #98, reset GPs in players df
        #97, reset all scores in players df
        #96, create schedule
        #90, create team,
        #91, city draft
        #92, simulate match
        #93, run week
        
        choice = input("Select an option (1-9): ").strip()
        
        if choice == "1":
            add_players()
        elif choice == "2":
            view_teams()
        elif choice == "3":
            view_active_roster()
        elif choice == "4":
            add_player_team()
        elif choice == "5":
            view_player_teams()
        elif choice == "6":
            player_draft()
        elif choice == "7":
            view_player_matchup()
        elif choice == "8":
            view_player_schedule()
        elif choice == "9":
            manage_team()

        #secret options
        elif choice =="90":
            create_team()
        elif choice =="91":
            city_draft()
        elif choice =="92":
            simulate_match()
        elif choice =="93":
            run_week()
        elif choice == "96":
            create_schedule()
        elif choice == "97":
            reset_GPs(reset_TPs = True)
        elif choice == "98":
            reset_GPs(reset_TPs = False)
        elif choice == "99":
            add_def_players()
        else:
            print("Invalid option, please try again.")
