# src/fetch_injuries.py

from nbainjuries import injury
from datetime import datetime

def get_injuries():
    """
    Fetch NBA injuries for today using nbainjuries package.
    Returns a dictionary:
    {
        "Boston Celtics": [
            {"player": "Jaylen Brown", "status": "Questionable", "note": "Right Knee"},
            ...
        ],
        ...
    }
    """
    injuries_by_team = {}

    # Today's date, 5 PM snapshot (NBA injury report cutoff)
    now = datetime.now()
    snapshot_dt = datetime(year=now.year, month=now.month, day=now.day, hour=17, minute=0)

    try:
        data = injury.get_reportdata(snapshot_dt)
    except Exception as e:
        print("Error fetching injury report:", e)
        return {}

    # Check if data is a list of dicts
    if not data or not isinstance(data, list):
        print("Injury report returned unexpected format:", data)
        return {}

    for entry in data:
        # Only process dictionaries
        if not isinstance(entry, dict):
            continue

        team = entry.get("Team")
        player = entry.get("Player Name")
        status = entry.get("Current Status")
        reason = entry.get("Reason")

        if not team or not player:
            continue

        if team not in injuries_by_team:
            injuries_by_team[team] = []

        injuries_by_team[team].append({
            "player": player,
            "status": status,
            "note": reason
        })

    return injuries_by_team

# -----------------------------
# Test locally
# -----------------------------
if __name__ == "__main__":
    injuries = get_injuries()
    if not injuries:
        print("No injuries found or unexpected report format.")
    for team, players in injuries.items():
        print(f"Team: {team}")
        for p in players:
            print(f" - {p['player']} ({p['status']}): {p['note']}")
