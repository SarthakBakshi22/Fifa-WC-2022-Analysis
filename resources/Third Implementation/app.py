from flask import Flask, render_template, request, redirect
import matplotlib.pyplot as plt
from plot import readTweets,top5_teams_graph,top5_players_graph,compare_players,compare_teams
import time
app = Flask(__name__)
@app.route('/',methods = ["GET","POST"])
def index():
    readTweets()
    return render_template('index.html')
 
@app.route('/myplayer',methods = ["GET","POST"])
def player():
    stratDate=request.form.get('start')
    endDate=request.form.get('end')
    print(type(stratDate))
    print(stratDate)


    p1 = request.form.get('player1')
    p2= request.form.get('player2')
    print(p1)
    print(type(p1))
    print(p2)
    print(type(p2))

    compare_players(stratDate,endDate,p1,p2)
    time.sleep(10)
    return render_template('myplayer.html')
    
    


@app.route('/myteams',methods = ["GET","POST"])
def team():
    stratDate=request.form.get('start')
    endDate=request.form.get('end')
    print(type(stratDate))
    print(stratDate)

    t1 = request.form.get('team1')
    t2= request.form.get('team2')
    option = request.form.get('option')
    print(t1)
    print(type(t1))
    print(t2)
    print(type(t2))

    compare_teams(stratDate,endDate,t1,t2)
    
    time.sleep(10)
    return render_template('myteams.html')


@app.route('/topplay',methods = ["GET","POST"])
def one():
    
    top5_players_graph()
    return render_template('checkplot_1.html')

@app.route('/topteam',methods = ["GET","POST"])
def two():
    
    top5_teams_graph()
    return render_template('checkplot_2.html')

if __name__ == '__main__':
   app.run()
