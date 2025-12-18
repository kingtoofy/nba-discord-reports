# src/fetch_injuries.py

import requests

NBA_INJURIES_URL = "https://raw.githubusercontent.com/mxufc29/nbainjuries/main/data/injury-report.json"

def get_injuries():
    """
    Fetch NBA injuries from nbainjuries JSON.
    Returns dict: team -> list of injured players
    """
    try:
        response = requests.get(NBA_INJURIES_URL, timeout=10)
        response.raise_for_status()
        data = response.json()

        injuries = {}
        for team_entry in data.get("teams", []):
            team_name = team_entry.get("team")
            players = team_entry.get("players", [])
            injuries[team_name] = []
            for p in players:
                injuries[team_name].append({
                    "player": p.get("name"),
                    "status": p.get("status"),
                    "note": p.get("injury", "")
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
