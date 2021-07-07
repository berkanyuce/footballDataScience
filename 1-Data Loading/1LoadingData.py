#Load in Statsbomb competition and match data

import json

#Load competitions.json
with open('C:/Users/Berkan/Desktop/Football/Data/StasBomb Dataset/open-data-master/data/competitions.json') as f:
    competitions = json.load(f)
    
#If we look inside the competition, we can see what the competitions we have.
#In this example we are gonna use Womens World Cup 2019. So it's ID is 72
competition_id = 72

#We need to all matches from this competition. So we should load this competition's matches
#from Statsbomb data.
with open('C:/Users/Berkan/Desktop/Football/Data/StasBomb Dataset/open-data-master/data/matches/' +str(competition_id) + '/30.json') as f:
    matches = json.load(f)
    
"""
    
#print all match results
for match in matches:
    home_team_name = match['home_team']['home_team_name']
    away_team_name = match['away_team']['away_team_name']
    home_score = match['home_score']
    away_score = match['away_score']
    describe_text = 'The match between ' + home_team_name + ' and ' + away_team_name
    result_text = ' finished ' + str(home_score) + ' : ' + str(away_score)
    print(describe_text + result_text)
    
#Lets find a match we are interested in
home_team_required = "England Women's"
away_team_required = "Sweden Women's"

#Find ID for the match
for match in matches:
    home_team_name = match['home_team']['home_team_name']
    away_team_name = match['away_team']['away_team_name']
    if(home_team_name == home_team_required) and (away_team_name == away_team_required):
        match_id_required = match['match_id']
print(home_team_required + ' vs ' + away_team_required + ' has id: ' + str(match_id_required))

"""
#Lets do samething for Men's World Cup

#Men World Cup ID is 43 as called 'FIFA World Cup'
competition_id = 43

#All matches from world cup. This time our json's name is '3.json'
with open('C:/Users/Berkan/Desktop/Football/Data/StasBomb Dataset/open-data-master/data/matches/' +str(competition_id) + '/3.json') as f:
    matches_men = json.load(f)
    
 
#print all match results
for match in matches_men:
    home_team_name = match['home_team']['home_team_name']
    away_team_name = match['away_team']['away_team_name']
    home_team_score = match['home_score']
    away_team_score = match['away_score']
    describe_text = 'The match between ' + home_team_name + ' vs ' + away_team_name
    result_text = ' finished ' + str(home_team_score) + ' : ' + str(away_team_score)
    print(describe_text + result_text)
    
#Find Sweden vs England
home_team_required = 'Sweden'
away_team_required = 'England'

#Find the England vs Sweden ID
for match in matches_men:
    home_team_name = match['home_team']['home_team_name']
    away_team_name = match['away_team']['away_team_name']
    if(home_team_name == home_team_required) and (away_team_name == away_team_required):
        match_id_required = match['match_id']
print(home_team_required + ' vs ' + away_team_required + ' has id: ' + str(match_id_required))

#Print all Sweden's results
team_required = 'Sweden'
for match in matches_men:
    home_team_name = match['home_team']['home_team_name']
    away_team_name = match['away_team']['away_team_name']
    if(home_team_name == team_required) or (away_team_name == team_required):
        describe_text = 'The match between ' + home_team_name + ' vs ' + away_team_name
        result_text = ' finished ' + str(home_team_score) + ' : ' + str(away_team_score)
        print(describe_text + result_text)

#Data Resource: Statsbomb