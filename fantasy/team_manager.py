import pandas as pd
import csv
from tabulate import tabulate
from config import POSITIONS, PLAYER_TEAM_CSV_FILE, CSV_FILE


def get_droppable_indices(picked_pos):
    droppable = list(range(11, 16))  # Bench is always droppable

    if picked_pos == "QB":
        droppable.append(2)
    elif picked_pos == "RB":
        droppable += [3, 4, 8]  # RB1, RB2, FLEX
    elif picked_pos == "WR":
        droppable += [5, 6, 8]  # WR1, WR2, FLEX
    elif picked_pos == "TE":
        droppable += [7, 8]     # TE, FLEX
    elif picked_pos == "K":
        droppable.append(9)
    elif picked_pos == "DEF":
        droppable.append(10)

    return droppable

def swap_positions(row, player_to_start, player_pos):
    # Maps for active positions
    single_pos_map = {
        "QB": 2,
        "K": 9,
        "DEF": 10
    }

    multi_pos_map = {
        "RB": [3, 4, 8],    # RB1, RB2, FLEX
        "WR": [5, 6, 8],    # WR1, WR2, FLEX
        "TE": [7, 8],       # TE, FLEX
    }

    if player_pos in single_pos_map:
        pos_index = single_pos_map[player_pos]
        current_starter = row[pos_index]
        row[pos_index] = player_to_start

        for i in range(11, 16):  # Bench slots
            if row[i] == player_to_start:
                row[i] = current_starter
                break

    elif player_pos in multi_pos_map:
        eligible_slots = multi_pos_map[player_pos]
        options = []

        print(f"\nEligible positions to replace with {player_to_start}:")
        for idx in eligible_slots:
            options.append((idx, row[idx]))
            print(f"{len(options)}: {row[idx]} (Slot Index {idx})")

        print()
        choice = input("Choose a player to replace (enter number): ")
        try:
            chosen = int(choice) - 1
            if chosen < 0 or chosen >= len(options):
                print("Invalid choice. Try again.")
                return False  # signal failure to swap

            slot_index, current_starter = options[chosen]
            row[slot_index] = player_to_start

            for i in range(11, 16):
                if row[i] == player_to_start:
                    row[i] = current_starter
                    break
        except ValueError:
            print("Not a valid number. Try again.")
            return False  # signal failure

    else:
        print("Invalid position. No action taken.")
        return False

    return True  # success

def manage_team(team_name = None):
    print()
    if team_name == None:
        team_name = input("Team Owner: ")
    try:
        players_df = pd.read_csv(CSV_FILE)
    except:
        print("Invalid team name, try again")
        manage_team()

    active_players = []
    bench_players = []

    with open(PLAYER_TEAM_CSV_FILE, "r") as file:
        reader = csv.reader(file)
        #next(reader)  # Skip the header row
        print("\n--- Current Teams ---")
        for row in reader:
            if row[0] == team_name:
                active_players.append(row[2]) #QB
                active_players.append(row[3]) #RB
                active_players.append(row[4]) #RB
                active_players.append(row[5]) #WR
                active_players.append(row[6]) #WR
                active_players.append(row[7]) #TE
                active_players.append(row[8]) #FLEX
                active_players.append(row[9]) #K
                active_players.append(row[10]) #DEF
                #bench
                bench_players.append(row[11])
                bench_players.append(row[12])
                bench_players.append(row[13])
                bench_players.append(row[14])
                bench_players.append(row[15])

    position_order = ['QB', 'RB', 'WR', 'TE', 'K', 'DEF']

    # Filter down a copy of the dataset to the relevant fields of the coach 1 team
    active_players_df = players_df.loc[
        players_df['Name'].isin(active_players),
        ['Name', 'Position', 'Player_Team', 'City_Team', 'GPs', 'TPs', 'Status']
    ].copy()

    active_players_df['Position'] = pd.Categorical(
        active_players_df['Position'],
        categories=position_order,
        ordered=True
    )

    active_players_df = active_players_df.sort_values('Position')
    print("Active Players:")
    print(tabulate(active_players_df, headers="keys", tablefmt="grid"))


    bench_players_df = players_df.loc[
        players_df['Name'].isin(bench_players),
        ['Name', 'Position', 'Player_Team', 'City_Team', 'GPs', 'TPs', 'Status']
    ].copy()
    print("Bench Players:")
    print(tabulate(bench_players_df, headers="keys", tablefmt="grid"))

    print()
    print("What would you like to do?")
    print("0.Go Back")
    print("1.Start a player from your bench")
    print("2.Add from Free Roster")
    choice = input("1-2: ")

    if choice == '0':
        pass
    elif choice == '1':
        swap_from_bench(active_players, bench_players, team_name)
    elif choice == '2':
        add_from_free_agents(team_name)


def swap_from_bench(active_players, bench_players, team_name):
    #we'll program it in a way where they have to choose someone from the bench first, then who they'll replace
    player_num = 1
    for player in bench_players:
       print(f"{player_num}: {player}")
       player_num += 1

    print()
    player_to_start = ""

    choice = input("Enter number of player you would like to start or type 0 to go back: ")
    if choice == '0':
        manage_team(team_name = team_name)
    if int(choice) - 1 > len(bench_players):
        print("Invalid Player, Try Again Bozo")
        swap_from_bench(active_players, bench_players, team_name)
    else:
        player_to_start = bench_players[int(choice) - 1]

    #get the players df, just to get the position of the player
    players_df = pd.read_csv(CSV_FILE)
    player_pos = players_df.loc[players_df['Name'] == player_to_start]['Position'].iloc[0]
    print(player_pos)

    #If we're bringing in a QB, K, or DEF, we only have one option on who to sub out, so we don't need to ask the user who
    # Step 1: Read in all rows
    with open(PLAYER_TEAM_CSV_FILE, "r") as file:
        reader = list(csv.reader(file))

    # Step 2: Modify the matching team row in memory
    for i in range(len(reader)):
        if reader[i][0] == team_name:
            if swap_positions(reader[i], player_to_start, player_pos):
                print(f"{player_to_start} has been moved to the starting lineup.")
            else:
                print("Swap failed. Try again.")
                return swap_from_bench(active_players, bench_players, team_name)
            break

    # Step 3: Write everything back to the CSV file
    with open(PLAYER_TEAM_CSV_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(reader)

def add_from_free_agents(team_name):
    players_df = pd.read_csv(CSV_FILE)

    print("\nWhat position do you want to pick up? (e.g., QB, RB, WR, TE, K, DEF)")
    position = input("Enter position: ").strip().upper()

    # Step 1: Filter to active, unclaimed players at that position
    available_players = players_df[
        (players_df["Position"] == position) &
        (players_df["Status"] == "Active") &
        #If you want to allow the player to pickup players on the bench, comment the line above and uncomment the one below
        #((players_df["Status"] == "Active") | (players_df["Status"] == "Benched")) &
        (players_df["Player_Team"] == "No Team")
    ]

    if available_players.empty:
        print(f"\nNo free agents available at {position} right now.")
        return

    available_players = available_players.reset_index(drop=True)
    display_df = available_players[['Name', 'Position', 'Player_Team', 'City_Team', 'GPs', 'TPs', 'Status']]

    print(tabulate(display_df, headers="keys", tablefmt="grid"))
    print(f"\nFree agents available at {position}:\n")
    for i, player in available_players.iterrows():
        print(f"{i+1}: {player['Name']}")

    choice = input("\nEnter the number of the player you'd like to pick up, or 0 to cancel: ")
    if choice == '0':
        print("Canceled pickup.\n")
        return

    try:
        choice_index = int(choice) - 1
        if choice_index < 0 or choice_index >= len(available_players):
            print("Invalid choice. Try again.")
            return add_from_free_agents(team_name)

        picked_player = available_players.loc[choice_index, "Name"]
        picked_pos = available_players.loc[choice_index, "Position"]

        # Step 2: Load team CSV and get team row
        with open(PLAYER_TEAM_CSV_FILE, "r") as file:
            team_data = list(csv.reader(file))

        for i, row in enumerate(team_data):
            if row[0] == team_name:
                team_row = row
                team_index = i
                display_name = row[1]
                break
        else:
            print("Team not found.")
            return

        # Step 3: Show players that can be dropped
        print("\nChoose a player to drop:")
        drop_options = []
        allowed_indices = get_droppable_indices(picked_pos)

        for idx in allowed_indices:
            player_name = team_row[idx]
            drop_options.append((idx, player_name))
            print(f"{len(drop_options)}: {player_name}")

        drop_choice = input("\nEnter number of player to drop, or 0 to cancel: ")
        if drop_choice == '0':
            print("Canceled pickup.\n")
            return

        drop_index = int(drop_choice) - 1
        if drop_index < 0 or drop_index >= len(drop_options):
            print("Invalid drop choice. Try again.")
            return add_from_free_agents(team_name)

        drop_slot_index, player_to_drop = drop_options[drop_index]

        # Step 4: Update team row
        team_row[drop_slot_index] = picked_player
        team_data[team_index] = team_row

        # Step 5: Update both players in player database
        players_df.loc[players_df["Name"] == picked_player, "Player_Team"] = display_name
        players_df.loc[players_df["Name"] == player_to_drop, "Player_Team"] = "No Team"

        # Step 6: Save everything
        with open(PLAYER_TEAM_CSV_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(team_data)

        players_df.to_csv(CSV_FILE, index=False)

        print(f"\n {picked_player} added to {team_name}. {player_to_drop} has been released to free agency.\n")

    except ValueError:
        print("Not a valid number. Try again.")
        return add_from_free_agents(team_name)

