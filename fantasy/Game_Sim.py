from calendar import week
import random
import pandas as pd
from IPython.display import display
from tabulate import tabulate
from config import CSV_FILE, TEAM_CSV_FILE, PLAYER_TEAM_CSV_FILE, CITY_SCHEDULE
import time


def simulate_match(home_team = None, away_team = None):
    from fantasy import get_player_by_pos, get_defense_skill, update_team_points
    #pre game set up, todo in future:set up this to auto run based off of schedule
    players_df = pd.read_csv(CSV_FILE)
    teams_df = pd.read_csv(PLAYER_TEAM_CSV_FILE)

    print()
    game_length = 60

    if(home_team == None or away_team == None):
        home_team = input("Home Team: ").strip()
        away_team = input("Away Team: ").strip()

    home_score = 0
    away_score = 0

    yds_to_td = 50 #value between 0-100, if its 0, then touchdown baby
    yds_to_fd = 10 #value between 0-10, if its 0, then first down baby
    downs = 0 #values between 0 and 4, 4 indicating a possession change
    play_num = 0

    live_viewing = input("Would you like to view the game live? ").strip()
    delay_time = 0
    if live_viewing == 'yes':
        delay_time = 1

    game_status = "Ongoing"
    offense_team = ""
    defence_team = ""
    coin_flip = random.choice([0,1])
    if coin_flip == 0:
        offense_team = home_team
        defence_team = away_team
    else:
        offense_team = away_team
        defence_team = home_team

    #adding this to calc defense score
    home_yds = 0
    away_yds = 0

    #We want to time sleep if it's a live game to make it easier to view
    time.sleep(delay_time)
    print(f"{offense_team} has won the coin flip and will be starting on offense")
    time.sleep(delay_time)
    offense_qb = get_player_by_pos('QB', offense_team, players_df).iloc[0]
    offense_wr1 = get_player_by_pos('WR', offense_team, players_df).iloc[0]
    offense_wr2 = get_player_by_pos('WR', offense_team, players_df).iloc[1]
    offense_rb1 = get_player_by_pos('RB', offense_team, players_df).iloc[0]
    offense_rb2 = get_player_by_pos('RB', offense_team, players_df).iloc[1]
    offense_rb1 = get_player_by_pos('RB', offense_team, players_df).iloc[0]
    offense_te = get_player_by_pos('TE', offense_team, players_df).iloc[0]
    offense_k = get_player_by_pos('K', offense_team, players_df).iloc[0]

    home_def = get_player_by_pos('DEF', home_team, players_df).iloc[0]
    away_def = get_player_by_pos('DEF', away_team, players_df).iloc[0]

    defense_skill = get_defense_skill(players_df, defence_team)
    starting_team = offense_team
    half_time_team = defence_team

    def switch_teams(halftime = False):
        nonlocal offense_team, defence_team, offense_qb, offense_wr1, offense_wr2, home_team, away_team
        nonlocal offense_rb1, offense_rb2, offense_te, offense_k, defense_skill, downs, yds_to_fd

        if(halftime):
            offense_team = half_time_team
            defence_team = starting_team
        else:
            if offense_team == home_team:
                offense_team = away_team
                defence_team = home_team
            else:
                offense_team = home_team
                defence_team = away_team


        offense_qb = get_player_by_pos('QB', offense_team, players_df).iloc[0]
        offense_wr1 = get_player_by_pos('WR', offense_team, players_df).iloc[0]
        offense_wr2 = get_player_by_pos('WR', offense_team, players_df).iloc[1]
        offense_rb1 = get_player_by_pos('RB', offense_team, players_df).iloc[0]
        offense_rb2 = get_player_by_pos('RB', offense_team, players_df).iloc[1]
        offense_rb1 = get_player_by_pos('RB', offense_team, players_df).iloc[0]
        offense_te = get_player_by_pos('TE', offense_team, players_df).iloc[0]
        offense_k = get_player_by_pos('K', offense_team, players_df).iloc[0]

        time.sleep(delay_time)
        print(f"{offense_qb['Name']} walks onto the field, fire in their eyes.")
        defense_skill = get_defense_skill(players_df, defence_team)
        downs = 0
        yds_to_fd = 10

    def update_score(score_change):
        nonlocal offense_team, home_score, away_score, home_team, away_team
        if offense_team == home_team:
            home_score = home_score + score_change
        else:
            away_score = away_score + score_change
    
    def update_player_pts(player_to_update, pt_change):
        nonlocal players_df

        player_name = player_to_update["Name"]
        player_to_update = players_df.loc[players_df["Name"] == player_name]
        current_gps = player_to_update["GPs"]
        current_tps = player_to_update["TPs"]

        players_df.loc[players_df["Name"] == player_name, "GPs"] = (current_gps + pt_change)
        players_df.loc[players_df["Name"] == player_name, "TPs"] = (current_tps + pt_change)

    def td_procedure(credit_player):
        nonlocal yds_to_td
        time.sleep(delay_time)
        print(f"TOUCHDOWN BY {credit_player}!!!")
        #update the score for initial score
        update_player_pts(credit_player, 6)
        update_score(6)

        rush_option = random.choice([0,1,2,3,4])
        if rush_option == 0: #1 in 5 chance, most times we should kick
            time.sleep(delay_time)
            print(f"{offense_qb['Name']} Trys to rush the ball over the line for an extra 2 points!")

            difficulty = defense_skill * random.uniform(0.75,1.20)
            num_to_beat = random.uniform(0, difficulty)

            if ((offense_qb['Strength']/2) * 0.8) + ((offense_qb['Gumption']/2) * 1.2)  >  num_to_beat:
                time.sleep(delay_time)
                print(f"EXTRA POINTS GOOD THANKS TO {offense_qb['Name']}!!")
                update_player_pts(offense_qb, 2)
                update_score(2)
            else:
                time.sleep(delay_time)
                print(f"{offense_qb['Name']} biffs their chanse for extra points")
        else:
            time.sleep(delay_time)
            print(f"{offense_k['Name']} is going for the kick!")
            num_to_beat = 15
            kick_value = random.uniform(0, offense_k['Accuracy'])
            time.sleep(delay_time)
            if(kick_value > num_to_beat):
                print(f"{offense_k['Name']} secures! the extra point!")
                update_player_pts(offense_k, 1)
                update_score(1)
            else:
                print(f"{offense_k['Name']} misses the shot!")

        #kick off
        starting_yd = random.uniform(20, 50)
        time.sleep(delay_time)
        print(f"{offense_k['Name']} kicks the ball to the {starting_yd} yard line.")
        yds_to_td = 100 - starting_yd

        switch_teams()

    #The game is starting
    print(f"{offense_qb['Name']} walks onto the field, fire in their eyes.")

    while game_status == "Ongoing":
        #once per game events
        if play_num == game_length - 1:
            game_status = "Ending"
            time.sleep(delay_time)
            print("Surely this is the last place of the game!")
        if play_num == game_length / 2:
            #Half time
            time.sleep(delay_time)
            print("That's halftime folks!")
            switch_teams(halftime=True)
            yds_to_td = 50
            yds_to_fd = 10
            downs = 0
        
        #repeatable events
        if downs == 3:
            #if we're really close, lets maybe rush to get that td, otherwise, kick
            if yds_to_td < 5:
                rush_option = random.choice([0,2])
                if rush_option == 0: #1 in 3 chance, most times we should kick
                    #rush da ball
                    time.sleep(delay_time)
                    print(f"{offense_qb['Name']} Trys to rush the ball over the line!")

                    difficulty = defense_skill * random.uniform(0.75,1.20)
                    num_to_beat = random.uniform(0, difficulty)

                    if ((offense_qb['Strength']/2) * 0.8) + ((offense_qb['Gumption']/2) * 1.2)  >  num_to_beat:
                        time.sleep(delay_time)
                        print(f"TOUCH DOWN BY {offense_qb['Name']}!!")
                        td_procedure(offense_qb)

                        if offense_team == home_team:
                            home_yds = home_yds + yds_to_td
                        else:
                            away_yds = away_yds + yds_to_td
                    else:
                        print(f"{offense_team} failed to get it done")
                        switch_teams()
                else: #kick da ball
                    time.sleep(delay_time)
                    print(f"{offense_k['Name']} is going for the kick!")
                    num_to_beat = 10
                    kick_value = random.uniform(0, offense_k['Accuracy'])
                    time.sleep(delay_time)
                    if(kick_value > num_to_beat):
                        print(f"{offense_k['Name']} secures! the field goal!")
                        update_player_pts(offense_k, 3)
                        update_score(3)

                        if offense_team == home_team:
                            home_yds = home_yds + yds_to_td
                        else:
                            away_yds = away_yds + yds_to_td
                    else:
                        print(f"{offense_k['Name']} misses the shot!")
                    switch_teams()
            else:
                #we're too far away to rush, so kick da ball
                time.sleep(delay_time)
                print(f"{offense_k['Name']} is going for the kick from the {yds_to_td} yard line!")
                
                num_to_beat = yds_to_td * 1.2
                kick_value = random.uniform(0, offense_k['Accuracy'])
                time.sleep(delay_time)
                if(kick_value > num_to_beat):
                    print(f"{offense_k['Name']} secures! the field goal!")
                    update_player_pts(offense_k, 3)
                    update_score(3)

                    if offense_team == home_team:
                            home_yds = home_yds + yds_to_td
                    else:
                        away_yds = away_yds + yds_to_td
                else:
                    print(f"{offense_k['Name']} misses the shot!")
                switch_teams()
        else:
            #we're not on the last down so no need to even consider kicking
            qb_choices = ["Long Pass", "Short Pass", "Short Pass", "Hand Off", "Rush"]
            accuracy = offense_qb['Accuracy']
            gumption = offense_qb['Gumption']
            wf = offense_qb['Wow_Factor']
            speed = offense_qb['Speed']
            strength = offense_qb['Strength']
            finesse = offense_qb['Finesse']
            qb_name = offense_qb['Name']

            #Long pass likes Accuracy and Wow Factor
            #Short pass likes Accuracy and Finesse
            #Hand off likes Finesse and Gumption
            #Rush likes Strength, Gumption, Speed, and Wow Factor

            #tip the odds of what the QB will do based off their stats
            #long pass
            if(accuracy + wf > 180):
                qb_choices.append("Long Pass")
            if(accuracy + wf > 165):
                qb_choices.append("Long Pass")
            if(accuracy + wf > 150):
                qb_choices.append("Long Pass")
            if(accuracy + wf > 133):
                qb_choices.append("Long Pass")
            if(accuracy + wf > 125):
                qb_choices.append("Long Pass")
            #short pass
            if(accuracy + finesse > 180):
                qb_choices.append("Short Pass")
            if(accuracy + finesse > 165):
                qb_choices.append("Short Pass")
            if(accuracy + finesse > 150):
                qb_choices.append("Short Pass")
            if(accuracy + finesse > 133):
                qb_choices.append("Short Pass")
            if(accuracy + finesse > 125):
                qb_choices.append("Short Pass")
            #Hand off
            if(gumption + finesse > 180):
                qb_choices.append("Hand Off")
            if(gumption + finesse > 165):
                qb_choices.append("Hand Off")
            if(gumption + finesse > 150):
                qb_choices.append("Hand Off")
            if(gumption + finesse > 133):
                qb_choices.append("Hand Off")
            if(gumption + finesse > 125):
                qb_choices.append("Hand Off")
            #Rush
            if(gumption + finesse + speed + wf > 375):
                qb_choices.append("Rush")
            if(gumption + finesse + speed + wf > 366):
                qb_choices.append("Rush")
            if(gumption + finesse + speed + wf > 350):
                qb_choices.append("Rush")
            if(gumption + finesse + speed + wf > 333):
                qb_choices.append("Rush")
            if(gumption + finesse + speed + wf > 325):
                qb_choices.append("Rush")

            qb_choice = random.choice(qb_choices)
            time.sleep(delay_time)

            if(qb_choice=="Long Pass"):
                #Choose who we target the throw to based off of finesse and speed stats of WR
                targets = [offense_wr1, offense_wr2]
                if(offense_wr1['Finesse'] + offense_wr1['Speed'] > offense_wr2['Finesse'] + offense_wr2['Speed']):
                    targets.append(offense_wr1)
                    #WR1 is signicantly better
                    if(offense_wr1['Finesse'] + offense_wr1['Speed'] - offense_wr2['Finesse'] + offense_wr2['Speed'] > 15):
                        targets.append(offense_wr1)
                else:
                    targets.append(offense_wr2)
                    #WR2 is signicantly better
                    if(offense_wr2['Finesse'] + offense_wr2['Speed'] - offense_wr1['Finesse'] + offense_wr1['Speed'] > 15):
                        targets.append(offense_wr2)

                target = random.choice(targets)
                print(f"{qb_name} throws the ball long to {target['Name']}")
                difficulty = defense_skill * random.uniform(0.75,1.20)
                if((target['Finesse'] * 1.2)/3 + (target['Speed'] * 0.75) / 3 + offense_qb['Accuracy'] / 3 > difficulty):
                    #The catch is successful
                    time.sleep(delay_time)
                    print("Catch successful!")
                    yds_gained = int(random.uniform(8,15))
                    if(target["Wow_Factor"] * 0.5 > difficulty):
                        yds_gained = int(yds_gained + random.uniform(1,30))
                        time.sleep(delay_time)
                        print("With a huge gain! Look at that stud go!")
                    if yds_gained > yds_to_td:
                        #touchdown
                        update_player_pts(offense_qb, 4)
                        td_procedure(target)
                    else:
                        yds_to_td = yds_to_td - yds_gained
                        if yds_gained > yds_to_fd:
                            print("First down!")
                            #first down
                            yds_to_fd = 10
                            downs = 0
                        else:
                            #success without fd or td
                            yds_to_fd = yds_to_fd - yds_gained
                            downs = downs + 1
                    print(f"Total yards gained: {yds_gained}")
                    if offense_team == home_team:
                        home_yds = home_yds + yds_gained
                    else:
                        away_yds = away_yds + yds_gained

                    update_player_pts(offense_qb, round(yds_gained / 25, 2))
                    update_player_pts(target, round(yds_gained / 25, 2))

                else:
                    print("Pass incomplete")
                    downs = downs + 1

            elif(qb_choice=="Short Pass"):
                #Choose who we target the throw to based off of finesse and Gumption stats of RB & TE
                targets = [offense_rb1, offense_rb2, offense_te, offense_te]
                if(offense_rb1['Finesse'] + offense_rb1['Gumption'] > offense_rb2['Finesse'] + offense_rb2['Gumption']):
                    targets.append(offense_rb1)
                    #RB1 is signicantly better
                    if(offense_rb1['Finesse'] + offense_rb1['Gumption'] - offense_rb2['Finesse'] + offense_rb2['Gumption'] > 15):
                        targets.append(offense_rb1)
                else:
                    targets.append(offense_rb2)
                    #RB2 is signicantly better
                    if(offense_rb2['Finesse'] + offense_rb2['Gumption'] - offense_rb1['Finesse'] + offense_rb1['Gumption'] > 15):
                        targets.append(offense_rb2)
                #unless your TE is better then both your RBS, they're likely to get overlooked
                if ((offense_te['Finesse'] + offense_te['Gumption'] > offense_rb1['Finesse'] + offense_rb1['Gumption'])
                    and 
                    (offense_te['Finesse'] + offense_te['Gumption'] > offense_rb2['Finesse'] + offense_rb2['Gumption'])):

                        targets.extend([offense_te, offense_te])

                target = random.choice(targets)
                print(f"{qb_name} passes the ball short to {target['Name']}")
                difficulty = defense_skill * random.uniform(0.75,1.1)
                if((target['Finesse'] * 1.2)/3 + (target['Gumption'] * 0.75) / 3 + offense_qb['Accuracy'] / 3 > difficulty):
                    #The catch is successful
                    time.sleep(delay_time)
                    print("Catch successful!")
                    yds_gained = int(random.uniform(1,9))
                    if yds_gained > yds_to_td:
                        update_player_pts(offense_qb, 4)
                        #touchdown
                        td_procedure(target)
                    else:
                        yds_to_td = yds_to_td - yds_gained
                        if yds_gained > yds_to_fd:
                            print("First down!")
                            #first down
                            yds_to_fd = 10
                            downs = 0
                        else:
                            yds_to_fd = yds_to_fd - yds_gained
                            downs = downs + 1
                    print(f"Total yards gained: {yds_gained}")
                    if offense_team == home_team:
                        home_yds = home_yds + yds_gained
                    else:
                        away_yds = away_yds + yds_gained

                    update_player_pts(offense_qb, round(yds_gained / 25, 2))
                    update_player_pts(target, round(yds_gained / 25, 2))
                else:
                    print("Pass incomplete")
                    downs = downs + 1

            elif(qb_choice=="Hand Off"):
                #Choose who we target the throw to based off of Strength and Gumption stats of RB
                targets = [offense_rb1, offense_rb2, offense_te]
                if(offense_rb1['Strength'] + offense_rb1['Gumption'] > offense_rb2['Strength'] + offense_rb2['Gumption']):
                    targets.append(offense_rb1)
                    #RB1 is signicantly better
                    if(offense_rb1['Strength'] + offense_rb1['Gumption'] - offense_rb2['Strength'] + offense_rb2['Gumption'] > 15):
                        targets.append(offense_rb1)
                else:
                    targets.append(offense_rb2)
                    #RB2 is signicantly better
                    if(offense_rb2['Strength'] + offense_rb2['Gumption'] - offense_rb1['Strength'] + offense_rb1['Gumption'] > 15):
                        targets.append(offense_rb2)

                target = random.choice(targets)
                print(f"{qb_name} hands the ball off to {target['Name']}")

                difficulty = defense_skill * random.uniform(0.75,1.20)
                if((target['Strength'] * 1.2)/3 + (target['Speed'] * 0.7) / 3 + (target['Finesse'] + 1.1) / 3 > difficulty):
                    #The hand off is successful
                    time.sleep(delay_time)
                    print(f"{target['Name']} Breaks past the defensive line!")
                    yds_gained = int(random.uniform(8,15))
                    if(target["Wow_Factor"] * 0.5 > difficulty):
                        yds_gained = int(yds_gained + random.uniform(1,30))
                        time.sleep(delay_time)
                        print("With a huge gain! Look at that stud go!")
                    if yds_gained > yds_to_td:
                        #touchdown
                        td_procedure(target)
                    else:
                        yds_to_td = yds_to_td - yds_gained
                        if yds_gained > yds_to_fd:
                            print("First down!")
                            #first down
                            yds_to_fd = 10
                            downs = 0
                        else:
                            yds_to_fd = yds_to_fd - yds_gained
                            downs = downs + 1
                    print(f"Total yards gained: {yds_gained}")
                    if offense_team == home_team:
                        home_yds = home_yds + yds_gained
                    else:
                        away_yds = away_yds + yds_gained

                    update_player_pts(target, round(yds_gained / 10, 2))
                else:
                    print("Aw Shucks, a sack")
                    if(offense_team == home_team):
                        update_player_pts(away_def, 1)
                    else:
                        update_player_pts(home_def, 1)
                    downs = downs + 1

            elif(qb_choice=="Rush"):
                print(f"{qb_name} is deciding to {qb_choice}")
                target = offense_qb
                difficulty = defense_skill * random.uniform(0.75,1.20)
                if((target['Strength'] * 1.2)/3 + (target['Speed'] * 0.7) / 3 + (target['Finesse'] + 1.1) / 3 > difficulty):
                    #The hand off is successful
                    time.sleep(delay_time)
                    print(f"{target['Name']} Breaks past the defensive line!")
                    yds_gained = int(random.uniform(8,15))
                    if(target["Wow_Factor"] * 0.5 > difficulty):
                        yds_gained = int(yds_gained + random.uniform(1,30))
                        time.sleep(delay_time)
                        print("With a huge gain! Look at that stud go!")
                    if yds_gained > yds_to_td:
                        #touchdown
                        td_procedure(target)
                    else:
                        yds_to_td = yds_to_td - yds_gained
                        if yds_gained > yds_to_fd:
                            print("First down!")
                            #first down
                            yds_to_fd = 10
                            downs = 0
                        else:
                            yds_to_fd = yds_to_fd - yds_gained
                            downs = downs + 1
                    print(f"Total yards gained: {yds_gained}")
                    if offense_team == home_team:
                        home_yds = home_yds + yds_gained
                    else:
                        away_yds = away_yds + yds_gained

                    update_player_pts(target, round(yds_gained / 10, 2))
                else:
                    print("Aw Shucks, a sack")
                    downs = downs + 1

        if game_status == "Ending":
            #Do we need overtime
            if home_score == away_score:
                time.sleep(delay_time)
                print("What a close game! We're going to overtime!")
                game_length = game_length + int(game_length/4)
                game_status = "Ongoing"
            else:
                time.sleep(delay_time)
                print("That's the game!")
                print()
        play_num = play_num + 1
    
    print(f"{home_team} Score: {home_score}")
    print(f"{away_team} Score: {away_score}")

    #update city team W/L record
    if home_score > away_score:
        update_team_points(winning_team = home_team, losing_team = away_team, team_type="City Team")
    else:
        update_team_points(winning_team = away_team, losing_team = home_team, team_type="City Team")

    #score defense
    if(home_score >= 35):
        update_player_pts(away_def, -4)
    elif(home_score >= 28):
        update_player_pts(away_def, -1)
    elif(home_score >= 21):
        update_player_pts(away_def, 0)
    elif(home_score >= 14):
        update_player_pts(away_def, 1)
    elif(home_score >= 7):
        update_player_pts(away_def, 4)
    elif(home_score >= 1):
        update_player_pts(away_def, 7)
    else:
        update_player_pts(away_def, 10)

    if(away_score >= 35):
        update_player_pts(home_def, -4)
    elif(away_score >= 28):
        update_player_pts(home_def, -1)
    elif(away_score >= 21):
        update_player_pts(home_def, 0)
    elif(away_score >= 14):
        update_player_pts(home_def, 1)
    elif(away_score >= 7):
        update_player_pts(home_def, 4)
    elif(away_score >= 1):
        update_player_pts(home_def, 7)
    else:
        update_player_pts(home_def, 10)

    # Select only the desired columns
    display_df = players_df[["Name", "Position", "Species", "Projected_Skill", "City_Team", "Player_Team", "Status", "GPs", "TPs"]]
    home_team_display = display_df[
        (display_df["City_Team"] == home_team) & (display_df["Status"] != "Benched")
    ]
    away_team_display = display_df[
        (display_df["City_Team"] == away_team) & (display_df["Status"] != "Benched")
    ]
    # Sort by best preforming person on team
    display_home = home_team_display.sort_values(by="GPs", ascending=False)
    display_away = away_team_display.sort_values(by="GPs", ascending=False)

    print(tabulate(display_home, headers="keys", tablefmt="grid"))
    print(tabulate(display_away, headers="keys", tablefmt="grid"))

    # Save updates to CSV
    players_df.to_csv(CSV_FILE, index=False)


def run_week(week_number=None):
    if week_number is None:
        week_number = input("What week would you like to run? ")
    week_number = str(week_number).strip()

    city_schedule_df = pd.read_csv(CITY_SCHEDULE)

    home_col = f"H{week_number}"
    away_col = f"A{week_number}"

    if home_col not in city_schedule_df.columns or away_col not in city_schedule_df.columns:
        print(f"Week {week_number} does not exist in the schedule.")
        return

    print(f"Running matchups for Week {week_number}...")

    for i in range(len(city_schedule_df)):
        home_team = city_schedule_df.at[i, home_col]
        away_team = city_schedule_df.at[i, away_col]

        if home_team == "BYE" or away_team == "BYE":
            print(f"Week {week_number}, Row {i + 1}: BYE week, no match.")
            continue

        print(f"Simulating: {home_team} vs {away_team}")
        simulate_match(home_team=home_team, away_team=away_team)
