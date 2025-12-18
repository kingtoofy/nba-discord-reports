# src/fetch_injuries.py

import os
import requests

RAPIDAPI_URL = "https://sports-information.p.rapidapi.com/nba/injuries"
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

def get_injuries():
    """
    Fetch NBA injuries from RapidAPI Sports Information.
    Returns a dict of team -> list of injured players
    """
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "sports-information.p.rapidapi.com"
    }

    try:
        response = requests.get(RAPIDAPI_URL, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        injuries = {}
        for team in data.get("teams", []):
            team_name = team.get("name")
            players = team.get("players", [])
            injuries[team_name] = []
            for p in players:
                injuries[team_name].append({
                    "player": p.get("name"),
                    "status": p.get("status"),
                    "note": p.get("description", "")
                })

        return injuries

    except requests.RequestException as e:
        print(f"Failed to fetch injuries: {e}")
        return {}

# -----------------------------
# Test locally
# -----------------------------
if __name__ == "__main__":
    injuries = get_injuries()
    for team, players in injuries.items():
        print(team)
        for p in players:
            print(f" - {p['player']} ({p['status']}): {p['note']}")
