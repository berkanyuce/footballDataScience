import pandas as pd
import functions as ff
import matplotlib.pyplot as plt
from mplsoccer import Pitch


#Read the data
DATADIR = '/Users/berkanyuce/Google Drive/Football Ders/Data/Metrica Sports/data'
game_id = 2

eventfile = DATADIR + '/Sample_Game_%d/Sample_Game_%d_RawEventsData.csv' % (game_id, game_id)
events = pd.read_csv(eventfile)

#Check what do we have by console.
events['Type'].value_counts()

#Metrica Sports pitch's coordinates are 1x1. But we want to work clearly.
#So, we change dimensions from 1x1 to 106x68
events = ff.to_metric_coordinates(events)
pitch_length = 106
pitch_width = 68

#Set home and away team
home_events = events[events['Team'] == 'Home']
away_events = events[events['Team'] == 'Away']

#Check home and away team's infos by console
home_events['Type'].value_counts()
away_events['Type'].value_counts()

#Set shots
shots = events[events['Type'] == 'SHOT']
home_shots = home_events[home_events['Type'] == 'SHOT']
away_shots = away_events[away_events['Type'] == 'SHOT']

#Shots have sub-types
home_shots['Subtype'].value_counts()
away_shots['Subtype'].value_counts()

#Which player took each shot?
home_shots['From'].value_counts()
away_shots['From'].value_counts()

#Get goals
home_goals = home_shots[home_shots['Subtype'].str.contains('-GOAL')].copy()
away_goals = away_shots[away_shots['Subtype'].str.contains('-GOAL')].copy()

#Convert Goals from second to minutes.
home_goals['Minutes'] = home_goals['Start Time [s]'] / 60.

#Setting pitch with MPLSoccer
pitch = Pitch(pitch_type='skillcorner', pitch_color='#22312b', line_color='#c7d5cc', pitch_length=pitch_length, pitch_width=pitch_width)
fig, ax = pitch.draw(figsize=(16, 11), constrained_layout=True, tight_layout=False)
fig.set_facecolor("#22312b")

#We have 3 goals. And their ids' are 198, 1118 and 1723. 
sc1 = pitch.scatter(home_goals['Start X'][198], home_goals['Start Y'][198],marker='football',
                    s=600, ax=ax, label='Shooter')
line = pitch.lines(home_goals['Start X'][198], home_goals['Start Y'][198],
                   home_goals['End X'][198], home_goals['End Y'][198], comet=True,
                   label='shot', color='white', ax=ax)
ax.set_title(f'Goal Position', fontsize=30, c='white')

#plot passing move in run up to goal.
#We should look inside the 'events' dataframe and we see what happaned before the goal.
#So I decided to look last 8 passes before the goal.

ff.plot_events(events, 190, 198, 'Passing Move In Run Up To First Goal')

#Until here we worked with even data. And now Let's go inside the tracking data

#Thanks to tracking_data function, our columns named by 'Home/Away_PlayerNumber_x/y' format
tracking_home = ff.tracking_data(DATADIR, game_id, 'Home')
tracking_away = ff.tracking_data(DATADIR, game_id, 'Away')

#Check on console.
tracking_home.columns

#We should convert coordinates from 1x1 to our 106x68 format
tracking_home = ff.to_metric_coordinates(tracking_home)
tracking_away = ff.to_metric_coordinates(tracking_away)

#Let's look a few player's first 60s performance.
#With metricasports data, We can get 25 observations of players per second.
#60 seconds x 25 fps = 1500 So our first 1500 rows give us first 60 seconds data.

#Setting pitch with MPLSoccer
pitch2 = Pitch(pitch_type='skillcorner', pitch_color='#22312b', line_color='#c7d5cc', pitch_length=pitch_length, pitch_width=pitch_width)
fig, ax = pitch.draw(figsize=(16, 11), constrained_layout=True, tight_layout=False)
fig.set_facecolor("#22312b")

ax.plot( tracking_home['Home_11_x'].iloc[:1500], tracking_home['Home_11_y'].iloc[:1500], 'r', MarkerSize = 1)
ax.plot( tracking_home['Home_1_x'].iloc[:1500], tracking_home['Home_1_y'].iloc[:1500], 'b', MarkerSize = 1)
ax.plot( tracking_home['Home_2_x'].iloc[:1500], tracking_home['Home_2_y'].iloc[:1500], 'g', MarkerSize = 1)
ax.plot( tracking_home['Home_3_x'].iloc[:1500], tracking_home['Home_3_y'].iloc[:1500], 'k', MarkerSize = 1)
ax.plot( tracking_home['Home_4_x'].iloc[:1500], tracking_home['Home_4_y'].iloc[:1500], 'c', MarkerSize = 1)
ax.set_title(f"Home Team's Player 11, 1, 2, 3, 4 Positions", fontsize=30, c='white')

#Plot position at kick off
fig, ax = ff.plot_frame(tracking_home.loc[51], tracking_away.loc[51], 'Line Up')

#Plot positions at goal
#ff.plot_events(events, 198, 199, 'Positions at Goal')
frame = events.loc[198]['Start Frame']
fig, ax = ff.plot_frame(tracking_home.loc[frame], tracking_away.loc[frame], 'Positions At First Goal')

#Homework-1
    #Second Goal
pitch5 = Pitch(pitch_type='skillcorner', pitch_color='#22312b', line_color='#c7d5cc', pitch_length=pitch_length, pitch_width=pitch_width)
fig, ax = pitch.draw(figsize=(16, 11), constrained_layout=True, tight_layout=False)
fig.set_facecolor("#22312b")

sc2 = pitch.scatter(home_goals['Start X'][1118], home_goals['Start Y'][1118],marker='football',
                    s=600, ax=ax, label='Shooter')
line = pitch.lines(home_goals['Start X'][1118], home_goals['Start Y'][1118],
                   home_goals['End X'][1118], home_goals['End Y'][1118], comet=True,
                   label='shot', color='white', ax=ax)
ax.set_title(f"Second Goal's Position", fontsize=30, c='white')

ff.plot_events(events, 1109, 1118, 'Passing Move In Run Up To Second Goal')

    #Third Goal
    
pitch6 = Pitch(pitch_type='skillcorner', pitch_color='#22312b', line_color='#c7d5cc', pitch_length=pitch_length, pitch_width=pitch_width)
fig, ax = pitch.draw(figsize=(16, 11), constrained_layout=True, tight_layout=False)
fig.set_facecolor("#22312b")

sc2 = pitch.scatter(home_goals['Start X'][1723], home_goals['Start Y'][1723],marker='football',
                    s=600, ax=ax, label='Shooter')
line = pitch.lines(home_goals['Start X'][1723], home_goals['Start Y'][1723],
                   home_goals['End X'][1723], home_goals['End Y'][1723], comet=True,
                   label='shot', color='white', ax=ax)
ax.set_title(f"Third Goal's Position", fontsize=30, c='white')

ff.plot_events(events, 1718, 1723, 'Passing Move In Run Up To Third Goal')

#Homework-2
home_9_shots = home_shots[home_shots['From'] == 'Player9']

pitch6 = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc')
fig, ax = pitch.draw(figsize=(16, 11), constrained_layout=True, tight_layout=False)
fig.set_facecolor("#22312b")
ax.set_title(f"Player 9's all shots and him goal", fontsize=30, c='white')


for i, shot in home_9_shots.iterrows():
    x = shot['Start X']
    y = shot['Start Y']
    
    goal = shot['Subtype'][-5:] == '-GOAL' 
    
    if goal:
        sc1 = pitch.scatter(x, y, ax=ax, c='white', s=250)
        plt.text(x, y, shot['From'], c='white')
    else:
        sc1 = pitch.scatter(x, y, ax=ax, c='white', s=250, alpha = 0.4)
        plt.text(x, y, shot['From'], c='white')
        
        
#Homework-3
#If we look Player 9's goals, we can see goal's 'Start Frame' is 73983.
#This means Goal's second x 25 Frame
fig, ax = ff.plot_frame(tracking_home.loc[73983], tracking_away.loc[73983], "Positions at Player 9's Goal")

#Homework-4
ff.player_ran_distance(tracking_home, tracking_home['Home_2_x'], tracking_home['Home_2_y'], 'Player 2')
ff.player_ran_distance(tracking_home, tracking_home['Home_9_x'], tracking_home['Home_9_y'], 'Player 9')




'''
Improvements:
    I will try to zip 'Positions At Goal' with 'Goal Position'. It looks bad apart (Uncompleted)
    I can write a function to plot goals and plot run up the goal. (Uncompleted)

Homeworks:
    1- Plot the passes and shot leading up to the second and third goals in the match
    2- Plot all the shots by Player 9 of the home team. use a different symbol and transparency for shots that resulted in goals
    3- Plot the positions of all players at Playe 9's goal
    4- Calculate how far each player ran

MetricaSports' free data is used in this example.
The data's link is here: https://github.com/metrica-sports/sample-data
'''