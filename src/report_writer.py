# src/report_writer.py

import os
from datetime import datetime, date
import requests
from src.fetch_injuries import get_injuries

# balldontlie for schedule
BALLEDONTLIE_GAMES_URL = "https://api.balldontlie.io/v1/games"
BALLEDONTLIE_API_KEY = os.getenv("BALLEDONTLIE_API_KEY")

def get_schedule():
    today = date.today().isoformat()
    params = {"dates[]": today}
    headers = {"Authorization": f"Bearer {BALLEDONTLIE_API_KEY}"} if BALLEDONTLIE_API_KEY else {}

    try:
        response = requests.get(BALLEDONTLIE_GAMES_URL, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json().get("data", [])
        schedule = [f"{g['visitor_team']['full_name']} vs {g['home_team']['full_name']}" for g in data]
        return schedule
    except requests.RequestException as e:
        return [f"Failed to fetch schedule: {e}"]

def daily_report():
    now = datetime.now()
    report = f"🏀 **NBA Daily Report** 🏀\n_Time: {now.strftime('%Y-%m-%d %H:%M:%S')}_\n\n"

    # Schedule
    schedule = get_schedule()
    report += "**Today's Schedule:**\n"
    if schedule:
        for game in schedule:
            report += f"• {game}\n"
    else:
        report += "No games scheduled today\n"
    report += "\n"

    # Injuries
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
    now = datetime.now()
    return f"🏀 **NBA Daily Picks** 🏀\n_Time: {now.strftime('%Y-%m-%d %H:%M:%S')}_\n\nSchedule + injuries enabled.\n"

# -----------------------------
# Test locally
# -----------------------------
if __name__ == "__main__":
    print(daily_report())
    print("\n\n")
    print(picks_report())
