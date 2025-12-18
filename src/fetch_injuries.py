import os
import requests

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
url = "https://sports-information.p.rapidapi.com/nba/injuries"

headers = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "sports-information.p.rapidapi.com"
}

response = requests.get(url, headers=headers, timeout=10)
data = response.json()

# Example output
for team in data.get("teams", []):
    print(team["name"])
    for player in team.get("players", []):
        print(f" - {player['name']} ({player['status']})")
