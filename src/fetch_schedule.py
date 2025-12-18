import requests
from datetime import datetime

SCOREBOARD_URL = "https://cdn.nba.com/static/json/liveData/scoreboard/todaysScoreboard_00.json"

def get_todays_games():
    response = requests.get(SCOREBOARD_URL)
    data = response.json()

    games = []

    for game in data["scoreboard"]["games"]:
        home = game["homeTeam"]["teamName"]
        away = game["awayTeam"]["teamName"]
        games.append(f"{away} @ {home}")

    return games
