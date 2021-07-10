import matplotlib.pyplot as plt
import json

#size of the pitch in yards.
#Statsbomb standarts are 120x80
pitchLengthX = 120
pitchWidthY = 80

#ID for England vs Sweden Womens World Cup
#We found it first example. Check it out!
match_id_required = 69301
home_team_required = "England Women's"
away_team_required = "Sweden Women's"

#Load in the data
file_name = str(match_id_required) + '.json'

#Load in all match events
with open('/Users/berkanyuce/Google Drive/Football Ders/Data/StasBomb Dataset/open-data-master/data/events/' + file_name) as data_file:
    data = json.load(data_file)

#Get the nested structure in to a data frame
#In other words, json to data frame
from pandas.io.json import json_normalize
df = json_normalize(data, sep = '_').assign(match_id = file_name[:-5])

#A dataframe of shots
shots = df.loc[df['type_name'] == 'Shot'].set_index('id')


'''
#Draw the pitch with FCPython
from FCPython import createPitch
(fig, ax) = createPitch(pitchLengthX, pitchWidthY, 'yards', 'gray')

#Plot the shots
for i, shot in shots.iterrows():
    x = shot['location'][0]
    y = shot['location'][1]
    
    goal = shot['shot_outcome_name'] == 'Goal'
    team_name = shot ['team_name']
    
    circleSize = 2
    #circleSize = np.sqrt(shot['shot_statsbomb_xg'] * 15) #Statsbomb has own expected goals function. With this function, shots's circles are resized.
    
    if (team_name == home_team_required):
        if goal:
            shotCircle = plt.Circle((x, pitchWidthY - y), circleSize, color='red')
            plt.text((x+1),pitchWidthY-y+1,shot['player_name']) 
        else:
            shotCircle=plt.Circle((x,pitchWidthY-y),circleSize,color="red")     
            shotCircle.set_alpha(.2)
    elif (team_name==away_team_required):
        if goal:
            shotCircle=plt.Circle((pitchLengthX-x,y),circleSize,color="blue") 
            plt.text((pitchLengthX-x+1),y+1,shot['player_name']) 
        else:
            shotCircle=plt.Circle((pitchLengthX-x,y),circleSize,color="blue")      
            shotCircle.set_alpha(.2)
    ax.add_patch(shotCircle)
    
    
plt.text(5,75,away_team_required + ' shots') 
plt.text(80,75,home_team_required + ' shots') 
     
fig.set_size_inches(10, 7)
fig.savefig('Output/shots.pdf', dpi=100) 
plt.show()

'''


#Let's try this example using MPLSoccer's Pitch
from mplsoccer.pitch import Pitch
pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc')
fig, ax = pitch.draw(figsize=(16, 11), constrained_layout=True, tight_layout=False)
fig.set_facecolor("#22312b")

for i, shot in shots.iterrows():
    x = shot['location'][0]
    y = shot['location'][1]
    
    goal = shot['shot_outcome_name'] == 'Goal'
    team_name = shot['team_name']
    
    if(team_name == home_team_required):
        if goal:
            sc1 = pitch.scatter(x, pitchWidthY-y, ax=ax, c='green', s=250)
            plt.text((x+1), pitchWidthY-y+1, shot['player_name'], c='white')
        else:
            sc1 = pitch.scatter(x, pitchWidthY-y, ax=ax, c='green', s=250, alpha=0.4)
    elif(team_name == away_team_required):
        if goal:
            sc2 = pitch.scatter(pitchLengthX-x, y, ax=ax, c='yellow', s=250)
            plt.text(pitchLengthX-x+1, y+1, shot['player_name'], c='white')
        else:
            sc1 = pitch.scatter(pitchLengthX-x+1, y+1, ax=ax, c='yellow', s=250, alpha=0.4)

  
plt.text(0,-2,away_team_required + ' shots', c='white') 
plt.text(105,-2,home_team_required + ' shots', c='white') 
     
fig.set_size_inches(15, 10)
#fig.savefig('Output/shots_mplsoccer.pdf', dpi=100) 

#Homeworks
#1, Create a dataframe of passes which contains all the passes in the match
#2, Plot the start point of every Sweden pass. Attacking left to right.
#3, Plot only passes made by Caroline Seger (she is Sara Caroline Seger in the database)
#4, Plot arrows to show where the passes went

pitch2 = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc')
fig, ax = pitch.draw(figsize=(16, 11), constrained_layout=True, tight_layout=False)
fig.set_facecolor("#22312b")


#A dataframe of passes
passes = df.loc[df['type_name'] == 'Pass'].set_index('id')

#Offside, Out, etc. are stated in column. But completed passes are stated by Nan.
#So I decided to fill all NaN values in pass_outcome_name column by Completed.
#I hope they are completed passes :)
passes['pass_outcome_name'].fillna('Completed', inplace=True)

for i, pas in passes.iterrows():
    x_start = pas['location'][0]
    y_start = pas['location'][1]
    
    x_end = pas['pass_end_location'][0]
    y_end = pas['pass_end_location'][1]
    
    completed = pas['pass_outcome_name'] == 'Completed'
    team_name = pas['team_name']
    
    ''' 
    #I disabled home_team's passes. Because the pitch looks like crazy.'
    if(team_name == home_team_required):
        if completed:
            pitch2.arrows(x_start, y_start,
            x_end, y_end, width=2,
            headwidth=10, headlength=10, color='#d9ed92', ax=ax, label='Completed passes')
        else:
            pitch2.arrows(x_start, y_start,
            x_end, y_end, width=2,
            headwidth=10, headlength=10, color='#52b69a', ax=ax, label='Other passes')
    '''
    if(team_name == away_team_required):
        if completed:
            if pas['player_name'] == 'Sara Caroline Seger':
                pitch2.arrows(x_start, y_start,
                x_end, y_end, width=2,
                headwidth=10, headlength=10, color='#560bad', ax=ax, label="Sara Caroline Seger's Completed passes")
            else:
                pitch2.arrows(x_start, y_start,
                x_end, y_end, width=2,
                headwidth=10, headlength=10, color='#ffbe0b', ax=ax, label='Completed passes')
            
        else:
            if pas['player_name'] == 'Sara Caroline Seger':
                pitch2.arrows(x_start, y_start,
                x_end, y_end, width=2,
                headwidth=10, headlength=10, color='#f72585', ax=ax, label="Sara Caroline Seger's other passes") 
            
            else:
                pitch2.arrows(x_start, y_start,
                x_end, y_end, width=2,
                headwidth=10, headlength=10, color='#fb5607', ax=ax, label='Other passes') 
            
plt.text(0,-2,away_team_required + ' passes', c='white') 
plt.text(105,-2,home_team_required + ' passes', c='white') 

#I have a problem. I want to plot Sara's passes to a new pitch.
#I created pitch3 and then I used 'pitch3.arrows()', arrows are still showed in pitch2.

#Suggstion:
    #Mplsoccer supports multiple plots in single plot. You can use it. (In adjusting the play layout)





