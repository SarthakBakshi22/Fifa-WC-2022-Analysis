import plotly.express as px
import pandas
from collections import OrderedDict
import numpy as np
# these libraries are optional
import json
import time
import pprint
import matplotlib.pyplot as plt
from datetime import datetime
import datetime as dttime
import time
print("\n\n................START CODE .................\n\n")
pp = pprint.PrettyPrinter(indent=4,sort_dicts=True)

top_teams=[]
top_players=[]
total_mentions={}
tweets = []


with open('/Users/trafalgar/Desktop/DSPipe/FlaskApp/Proj/FifaWCPlayers.txt') as f:
    top_players = f.readlines()


top_players = [x.strip() for x in top_players]
#print(top_players)
top_players.sort()
with open('//Users/trafalgar/Desktop/DSPipe/FlaskApp/Proj/FifaWCTeams.txt') as f:
    top_teams = f.readlines()
top_teams = [x.strip() for x in top_teams]
#print(top_teams)
top_teams.sort()

def readTweets():
    print("\n    READING ALL TWEETS\n")
    for line in open('result-twitter.json', 'r'):
        tweets.append(json.loads(line))



def top5_teams_graph():
    print("\n    SHOW TOP 5 TEAMS\n")
    count=0

    for player in top_teams:
        for tweet in tweets:
            if player in tweet['data']['text']:
                count+=1
        total_mentions[player] = count
        count=0
    sort_dict = sorted(total_mentions.items(), key=lambda x:x[1],reverse=True)

    sorted_team = dict(sort_dict)

    x_axis = list(sorted_team.keys())[:5]
    y_axis = list(sorted_team.values())[:5]

    print(x_axis)
    print(y_axis)

    fig = plt.figure(figsize = (10, 5))
    
    # creating the bar plot
    plt.bar(x_axis, y_axis, color ='palegreen', width = 0.4)
    
    plt.xlabel("Teams")
    plt.ylabel("Tweet Count")
    plt.title('Top 5 Tweeted Teams')
    plt.savefig('/Users/trafalgar/Desktop/DSPipe/FlaskApp/Proj/static/topteams.png')
    plt.close()
    fig = px.bar(x = x_axis, y = y_axis, title="Top 5 Tweeted TEAMS")
    fig.write_html("templates/checkplot_2.html")

def top5_players_graph():
    print("\n    SHOW TOP 5 PLAYERS\n")  
    count=0

    for player in top_players:
        for tweet in tweets:
            temp_p = player.split()
            if any(x in tweet['data']['text'] for x in temp_p):
                count+=1
        total_mentions[player] = count
        count=0
    sort_dict = sorted(total_mentions.items(), key=lambda x:x[1],reverse=True)

    sorted_team = dict(sort_dict)

    x_axis = list(sorted_team.keys())[:5]
    y_axis = list(sorted_team.values())[:5]

    # print(x_axis)
    # print(y_axis)

    fig = plt.figure(figsize = (10, 5))
    
    # creating the bar plot
    plt.bar(x_axis, y_axis, color ='cornflowerblue', width = 0.4)
    
    plt.xlabel("Players")
    plt.ylabel("Tweet Count")
    plt.title('Top 5 Tweeted Players')
    plt.savefig('/Users/trafalgar/Desktop/DSPipe/FlaskApp/Proj/static/topplayers.png')
    plt.close()

    fig = px.bar(x = x_axis, y = y_axis, title="Top 5 Tweeted Players")
    fig.write_html("templates/checkplot_1.html")

def compare_teams(startDate,endDate,t1,t2):
    print("\n    SHOW COMPARISON BETWEEN 2 TEAMS\n")

    print(startDate)
    print(type(startDate))
    str_date=startDate
    a = str_date.split('-')
    print(a)
    start_date = dttime.date(int(a[0]), int(a[1]), int(a[2]))
    #start_date = dttime.date(2022, 11, 1)
    
    # consider the end date as 2021-march 1 st
    ed_date=endDate
    b = ed_date.split('-')
    end_date = dttime.date(int(b[0]), int(b[1]), int(b[2]))
    
    # delta time
    delta = dttime.timedelta(days=1)

    myrange = []

    t1count=0
    t2count=0
    team1=''
    team2=''
    team1 = t1
    team1_counts=[]
    team2 = t2
    team2_counts=[]
    while (start_date <= end_date):
        t1count=0
        t2count=0
        for x in tweets:
            if str(start_date) in x['data']['created_at'] :
                if team1 in x['data']['text']:
                    t1count+=1
                if team2 in x['data']['text'] :
                    t2count+=1
        myrange.append(start_date.strftime("%Y-%m-%d"))
        start_date += delta
        team1_counts.append(t1count)
        team2_counts.append(t2count)


    plt.plot(myrange, team1_counts,label = team1)
    plt.plot(myrange, team2_counts,label = team2)
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.title(team1 + " VS " + team2)
    plt.legend()
    plt.savefig('/Users/trafalgar/Desktop/DSPipe/FlaskApp/Proj/static/compareTeam.png')
    plt.close()

def compare_players(startDate,endDate,p1,p2):
    print("\n    SHOW COMPARISON BETWEEN 2 PLayers\n")
    print(startDate)
    print(type(startDate))
    str_date=startDate
    a = str_date.split('-')
    print(a)
    player1=''
    player2=''
    start_date = dttime.date(int(a[0]), int(a[1]), int(a[2]))
    #start_date = dttime.date(2022, 11, 1)
    
    # consider the end date as 2021-march 1 st
    ed_date=endDate
    b = ed_date.split('-')
    end_date = dttime.date(int(b[0]), int(b[1]), int(b[2]))
    #end_date = startDate #dttime.date(2022, 12, 5)
    
    # delta time
    delta = dttime.timedelta(days=1)

    myrange = []

    p1count=0
    p2count=0
    player1 = p1
    temp_p1 = player1.split()
    player1_counts=[]
    player2 = p2
    temp_p2 = player2.split()
    player2_counts=[]
    while (start_date <= end_date):
        p1count=0
        p2count=0
        for x in tweets:
            #print(type(x['data']['created_at']))
            #print(x)
            if str(start_date) in x['data']['created_at'] :
                if any(i in x['data']['text'] for i in temp_p1):
                    p1count+=1
                if any(j in x['data']['text'] for j in temp_p2):
                    p2count+=1
        myrange.append(start_date.strftime("%Y-%m-%d"))
        start_date += delta
        player1_counts.append(p1count)
        player2_counts.append(p2count)

    plt.plot(myrange, player1_counts,label = player1)
    plt.plot(myrange, player2_counts,label = player2)
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.title(player1 + " VS " + player2)
    plt.legend()
    plt.savefig('/Users/trafalgar/Desktop/DSPipe/FlaskApp/Proj/static/comparePlayer.png')
    plt.close()
