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

    # Use today's date, 5:00 PM ET snapshot (NBA injury report cutoff)
    now = datetime.now()
    snapshot_dt = datetime(year=now.year, month=now.month, day=now.day, hour=17, minute=0)

    try:
        data = injury.get_reportdata(snapshot_dt)
    except Exception as e:
        print("Error fetching injury report:", e)
        return {}

    # Organize by team
    for entry in data:
        team = entry.get("Team")
        player = entry.get("Player Name")
        status = entry.get("Current Status")
        reason = entry.get("Reason")

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
        print("No injuries found or error occurred.")
    for team, players in injuries.items():
        print(f"Team: {team}")
        for p in players:
            print(f" - {p['player']} ({p['status']}): {p['note']}")
