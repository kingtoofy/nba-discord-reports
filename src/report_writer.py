# src/report_writer.py

import requests
from datetime import date, datetime
from src.fetch_injuries import get_injuries

BALLEDONTLIE_GAMES_URL = "https://api.balldontlie.io/v1/games"

def get_schedule():
    """
    Fetch today's NBA schedule using balldontlie API.
    Returns a list of matchups like ["LAL vs BOS", ...]
    """
    schedule = []
    today = date.today().isoformat()
    params = {"dates[]": today}

    try:
        response = requests.get(BALLEDONTLIE_GAMES_URL, params=params, timeout=10)
        response.raise_for_status()

        try:
            data = response.json().get("data", [])
        except ValueError:
            print("Response is not valid JSON:", response.text)
            return ["Failed to fetch schedule: invalid JSON"]

        for g in data:
            home = g["home_team"]["full_name"]
            away = g["visitor_team"]["full_name"]
            schedule.append(f"{away} vs {home}")

    except requests.RequestException as e:
        schedule.append(f"Failed to fetch schedule: {e}")

    return schedule

def daily_report():
    """
    Generate the daily report for Discord.
    """
    now = datetime.now()
    report = f"🏀 **NBA Daily Report** 🏀\n_Time: {now.strftime('%Y-%m-%d %H:%M:%S')}_\n\n"

    # Schedule
    schedule = get_schedule()
    report += "**Today's Schedule:**\n"
    if schedule:
        for game in schedule:
            report += f" - {game}\n"
    else:
        report += " - No games scheduled today\n"
    report += "\n"

    # Injuries (empty for now)
    injuries = get_injuries()
    report += "**Injury Report:**\n"
    if injuries:
        for team, players in injuries.items():
            report += f"**{team}**\n"
            if players:
                for p in players:
                    report += f" - {p['player']} ({p['status']}): {p['note']}\n"
            else:
                report += " - No injuries reported\n"
            report += "\n"
    else:
        report += "No injury data available today.\n"

    return report[:1900]

def picks_report():
    """
    Placeholder top picks report.
    """
    now = datetime.now()
    report = f"🏀 **NBA Top Picks of the Day** 🏀\n_Time: {now.strftime('%Y-%m-%d %H:%M:%S')}_\n\n"

    # Example static picks
    top_picks = [
        {"player": "Trae Young", "pick": "Over 28.5 P+R+A", "confidence": "92%"},
        {"player": "Jayson Tatum", "pick": "Under 30.5 P+R+A", "confidence": "88%"},
        {"player": "LeBron James", "pick": "Over 25.5 P", "confidence": "85%"},
    ]

    for pick in top_picks:
        report += f"{pick['player']} — {pick['pick']} (Confidence: {pick['confidence']})\n"

    return report[:1900]

# -----------------------------
# Test locally
# -----------------------------
if __name__ == "__main__":
    print(daily_report())
    print("\n\n")
    print(picks_report())
