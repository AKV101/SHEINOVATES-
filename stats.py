from flask import Flask, render_template, request
import os
import pandas as pd

app = Flask(__name__)

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

@app.route('/')
def tech():
    return render_template('tech.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    player_name = request.form['player_name']
    qb_result = qb_stats(player_name)
    wr_result = wr_stats(player_name)
    tight_result = tight_stats(player_name)
    
    return render_template('result.html', qb_result=qb_result, wr_result=wr_result, tight_result=tight_result)

if __name__ == '__main__':
    app.run(debug=True)
