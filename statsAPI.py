from flask import Flask, render_template, request
import requests
import os
from bs4 import BeautifulSoup
import pandas as pd
from requests import get

app = Flask(__name__)

@app.route('/')
def tech():
    return render_template('tech.html')



# CSV files from https://github.com/MarcLinderGit/NFL_Stats

def rbStats(player_name):
    df_rush = pd.read_csv(os.getcwd() + "/db_NFL/2023/player/week18/rushing.csv")
    df_rec = pd.read_csv(os.getcwd() + "/db_NFL/2023/player/week18/receiving.csv")
    player_statsRush = df_rush[df_rush['Player'] == player_name]
    player_statsRec = df_rec[df_rec['Player'] == player_name]
    
    td = player_statsRush['TD'].values[0] + player_statsRec['TD'].values[0]  * 6 
    yds = (player_statsRush['Rush Yds'].values[0] /10) + (player_statsRec['Yds'].values[0] /25)
    negTO = player_statsRush['Rush FUM'].values[0] + player_statsRec['Rec FUM'].values[0]

    totpts = td + yds - negTO

    return totpts / 17

def defStats(team_name):
    
    return

def flxStats(player_name):
    df_rush = pd.read_csv(os.getcwd() + "/db_NFL/2023/player/week18/rushing.csv")
    df_rec = pd.read_csv(os.getcwd() + "/db_NFL/2023/player/week18/receiving.csv")
    player_statsRush = df_rush[df_rush['Player'] == player_name]
    player_statsRec = df_rec[df_rec['Player'] == player_name]
    
    td = player_statsRush['TD'].values[0] + player_statsRec['TD'].values[0]  * 6 
    yds = (player_statsRush['Rush Yds'].values[0] /10) + (player_statsRec['Yds'].values[0] /25)
    negTO = player_statsRush['Rush FUM'].values[0] + player_statsRec['Rec FUM'].values[0]

    totpts = td + yds - negTO

    return totpts / 17

def kickStats(player_name):
    df_kick = pd.read_csv(os.getcwd() + "/db_NFL/2023/player/week18/field-goals.csv")
    player_statsKick = df_kick[df_kick['Player'] == player_name]
    print(player_statsKick)
    fgm = player_statsKick['FGM'].values[0] * 3
    fgMissed = (player_statsKick['Att'].values[0] - player_statsKick['FGM'].values[0]) * 4

    totpts = fgm - fgMissed

    return totpts / 17


@app.route('/calculate', methods=['POST'])
def calculate():
    player_name = request.form['player_name']
    rb_result = rbStats(player_name)
    kick_result = kickStats(player_name)
    
    
    return render_template('result.html', rb_result=rb_result, kick_result=kick_result)

if __name__ == '__main__':
    app.run(debug=False)