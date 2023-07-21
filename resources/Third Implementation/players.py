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
total_mentions={}
tweets = []


with open('/Users/pradnyabhalerao/Documents/DataSci/analysis/proj3/FifaWCPlayers.txt') as f:
    top_players = f.readlines()

top_players = [x.strip() for x in top_players]
#print(top_players)
top_players.sort()

def readTweets():
    print("\n    READING ALL TWEETS\n")
    for line in open('result-twitter.json', 'r'):
        tweets.append(json.loads(line))
readTweets()

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
    plt.savefig('/Users/pradnyabhalerao/Documents/DataSci/analysis/proj3/plots/topplayers.png')
    plt.close()

def compare_players():
    print("\n    SHOW COMPARISON BETWEEN 2 TEAMS\n")
    start_date = dttime.date(2022, 11, 1)
    
    # consider the end date as 2021-march 1 st
    end_date = dttime.date(2022, 12, 5)
    
    # delta time
    delta = dttime.timedelta(days=1)

    myrange = []

    p1count=0
    p2count=0
    player1 = 'Lionel Messi'
    temp_p1 = player1.split()
    player1_counts=[]
    player2 = 'Cristiano Ronaldo'
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


    print(myrange)
    # print(player1_counts)
    # print(player2_counts)

    plt.plot(myrange, player1_counts,label = player1)
    plt.plot(myrange, player2_counts,label = player2)
    plt.xlabel('Date')
    plt.ylabel('Count')
    plt.title(player1 + " VS " + player2)
    plt.legend()
    plt.savefig('/Users/pradnyabhalerao/Documents/DataSci/analysis/proj3/plots/comparePlayer.png')
    plt.close()

readTweets()
top5_players_graph()
compare_players()
