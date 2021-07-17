import csv
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Pitch
import numpy as np
import math

def to_metric_coordinates(data, field_dimen=(106., 68.)):
    x_columns = [c for c in data.columns if c[-1].lower() == 'x'] #Checks columns last charachter
    y_columns = [c for c in data.columns if c[-1].lower() == 'y']
    data[x_columns] = (data[x_columns] - 0.5) * field_dimen[0]
    data[y_columns] = (data[y_columns] - 0.5) * field_dimen[1]
    return data

def tracking_data(DATADIR, game_id, teamname):
    teamfile = '/Sample_Game_%d/Sample_Game_%d_RawTrackingData_%s_Team.csv' % (game_id, game_id, teamname)
    csvfile = open('{}/{}'.format(DATADIR, teamfile),'r')
    reader = csv.reader(csvfile)
    teamnamefull =next(reader)[3].lower()
    
    #Construct columns names
    jerseys = [x for x in next(reader) if x != ''] #Extract player jersey numbers from second row
    columns = next(reader)
    for i, j in enumerate(jerseys): #Create x&y column headers for each player
        columns[i*2+3] = "{}_{}_x".format(teamname, j)
        columns[i*2+4] = "{}_{}_y".format(teamname, j)
    columns[-2] = 'ball_x' #Columns headers for the x&y posiitons of the ball
    columns[-1] = 'ball_y'

    #Place into new dataframe end return it.
    tracking = pd.read_csv('{}/{}'.format(DATADIR, teamfile), names=columns, index_col='Frame', skiprows=3)
    return tracking

def plot_frame(hometeam, awayteam, title, figax=None, team_colors=('r', 'b'), field_dimen=(106.0, 68.0), include_player_velocities=False, PlayerMarkerSize=10, PlayerAlpha=0.7, annotate=False):
    if figax is None: # create new pitch 
        pitch = Pitch(pitch_type='skillcorner', pitch_color='#22312b', line_color='#c7d5cc', pitch_length=106, pitch_width=68)
        fig, ax = pitch.draw(figsize=(16, 11), constrained_layout=True, tight_layout=False)
        fig.set_facecolor("#22312b")
        
    else: # overlay on a previously generated pitch
        fig,ax = figax # unpack tuple
    # plot home & away teams in order
    for team,color in zip( [hometeam,awayteam], team_colors) :
        x_columns = [c for c in team.keys() if c[-2:].lower()=='_x' and c!='ball_x'] # column header for player x positions
        y_columns = [c for c in team.keys() if c[-2:].lower()=='_y' and c!='ball_y'] # column header for player y positions
        ax.plot( team[x_columns], team[y_columns], color+'o', MarkerSize=PlayerMarkerSize, alpha=PlayerAlpha ) # plot player positions
        if include_player_velocities:
            vx_columns = ['{}_vx'.format(c[:-2]) for c in x_columns] # column header for player x positions
            vy_columns = ['{}_vy'.format(c[:-2]) for c in y_columns] # column header for player y positions
            ax.quiver( team[x_columns], team[y_columns], team[vx_columns], team[vy_columns], color=color, scale_units='inches', scale=10.,width=0.0015,headlength=5,headwidth=3,alpha=PlayerAlpha)
        if annotate:
            [ ax.text( team[x]+0.5, team[y]+0.5, x.split('_')[1], fontsize=10, color=color  ) for x,y in zip(x_columns,y_columns) if not ( np.isnan(team[x]) or np.isnan(team[y]) ) ] 
    # plot ball
    ax.plot( hometeam['ball_x'], hometeam['ball_y'], 'ko', MarkerSize=6, alpha=1.0, LineWidth=0)
    ax.set_title(f"%s"%title, fontsize=30, c='white')

    return fig,ax

def plot_events(events, range_x, range_y, title):
    pitch = Pitch(pitch_type='skillcorner', pitch_color='#22312b', line_color='#c7d5cc', pitch_length=106, pitch_width=68)
    fig, ax = pitch.draw(figsize=(16, 11), constrained_layout=True, tight_layout=False)
    fig.set_facecolor("#22312b")
    for i in range(range_x, range_y):
        x_start = events['Start X'][i]
        y_start = events['Start Y'][i]
    
        x_end = events['End X'][i]
        y_end = events['End Y'][i]
    
        if i == range_y:
            return fig, ax
    
        pitch.arrows(x_start, y_start,
                     x_end, y_end, width=2,
                     headwidth=10, headlength=10, color='orange', ax=ax, label="Run up to goal.")
        pitch.annotate(events['Type'][i] +' '+ events['From'][i], (x_start+1.5, y_start+0.5), ax=ax, size=15, c='white')
        ax.set_title('%s' %(title), fontsize=30, c='white' )
    
def player_ran_distance(tracking, x, y, player):
    distance = 0
    for i in range(1, len(tracking)):
        distance += math.sqrt((x[i+1] - x[i])**2 + (y[i+1] - y[i])**2)
    print("%s's ran distance is: %d meters" % (player, distance))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

#I watched 'Friends of Tracking Tutorial: https://www.youtube.com/watch?v=8TrleFklEsE'
#I tried to write all codes myself. I copied only plot_frame function


 