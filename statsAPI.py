from flask import Flask, render_template, request
import requests
import os
import pandas as pd
from requests import get

app = Flask(__name__)

@app.route('/')
def tech():
    return render_template('DraftHelper.html')



# CSV files from https://github.com/MarcLinderGit/NFL_Stats


def qb_stats(player_name):
    try:
        dfr = pd.read_csv(os.getcwd() + "/db_NFL/2023/player/week18/rushing.csv")
        dfp = pd.read_csv(os.getcwd() + "/db_NFL/2023/player/week18/passing.csv")
        dfi = pd.read_csv(os.getcwd() + "/db_NFL/2023/player/week18/interceptions.csv")
    except FileNotFoundError:
        print("CSV files not found.")
        return 0  # Handle case where CSV files are not found
    
    try:
        rushing_touchdown = dfr[dfr['Player'] == player_name]
        passing_touchdown = dfp[dfp['Player'] == player_name]
        intercepted_pass = dfi[dfi['Player'] == player_name]
    except KeyError:
        print("KeyError: Player data not found.")
        return 0  # Handle case where player data is not found

    if rushing_touchdown.empty or passing_touchdown.empty or intercepted_pass.empty:
        print("Player data not found.")
        return 0  # Handle case where player data is not found

    td = rushing_touchdown['TD'].values[0] + passing_touchdown['TD'].values[0] + intercepted_pass['TD'].values[0] * 6 
    yds = (rushing_touchdown['Rush Yds'].values[0] / 10) + (passing_touchdown['Pass Yds'].values[0] / 25)
    neg = intercepted_pass['INT Yds'].values[0] * -2

    totpts = td + yds - neg

    return totpts / 17

def wr_stats(player_name):
    try:
        dfr = pd.read_csv(os.getcwd() + "/db_NFL/2023/player/week18/receiving.csv")
        receiving = dfr[dfr['Player'] == player_name]
    except FileNotFoundError:
        print("Receiving CSV file not found.")
        return 0  # Handle case where CSV file is not found
    
    try:
        td = receiving['TD'].values[0] * 6 
        yds = receiving['Yds'].values[0] / 25
        negTO = receiving['Rec FUM'].values[0] * -2
    except KeyError:
        print("KeyError: Player data not found.")
        return 0  # Handle case where player data is not found

    totpts = td + yds - negTO

    return totpts / 17

def tight_stats(player_name):
    return wr_stats(player_name)  # Assuming the logic for tight ends is the same as for wide receivers




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
    
    df_fum = pd.read_csv(os.getcwd() + "/db_NFL/2023/team/week18/defense/fumbles.csv")
    df_intercept = pd.read_csv(os.getcwd() + "/db_NFL/2023/team/week18/defense/interceptions.csv")
    df_passing = pd.read_csv(os.getcwd() + "/db_NFL/2023/team/week18/defense/passing.csv")
    
    player_statsFum = df_fum[df_fum['Team'] == team_name]
    player_statsInter = df_intercept[df_intercept['Team'] == team_name]
    player_statsPass = df_passing[df_passing['Team'] == team_name]
    
    td = (player_statsFum['FR TD'].values[0] + player_statsInter['INT TD'].values[0])  * 6 
    sks = player_statsPass['Sck'].values[0] * 2
    fums = (player_statsFum['FF'].values[0] * 2) + (player_statsFum['FR'].values[0] * 2)
    ints = player_statsInter['INT TD'].values[0] * 4
    totpts = td + sks + fums + ints

    return totpts / 17

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
    fgm = player_statsKick['FGM'].values[0] * 3
    fgMissed = (player_statsKick['Att'].values[0] - player_statsKick['FGM'].values[0]) * 4

    totpts = fgm - fgMissed

    return totpts / 17


@app.route('/calculate', methods=['POST'])
def calculate():
    rb_name1 = request.form['rb1']
    rb_name2 = request.form['rb2']
    kick_name = request.form['kicker']
    flex_name = request.form['flex']
    def_name = request.form['defense']
    qb_name = request.form['qb']
    wr_name1 = request.form['wr1']
    wr_name2 = request.form['wr2']
    te_name = request.form['te']
    
    
    rb_result = rbStats(rb_name1)
    rb_result2 = rbStats(rb_name2)
    kick_result = kickStats(kick_name)
    flex_result = flxStats(flex_name)
    def_result = defStats(def_name)
    qb_result = qb_stats(qb_name)
    wr_result = wr_stats(wr_name1)
    wr_result2 = wr_stats(wr_name2)
    tight_result = tight_stats(te_name)
    
    tot = rb_result + kick_result + flex_result + def_result + rb_result2 + tight_result + qb_result + wr_result + wr_result2
    return render_template('result.html', tot_result=tot)

if __name__ == '__main__':
    app.run(debug=False)