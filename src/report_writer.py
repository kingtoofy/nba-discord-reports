# src/report_writer.py

import os
from datetime import datetime, date
import requests
from src.fetch_injuries import get_injuries

# balldontlie API for schedule
BALLEDONTLIE_GAMES_URL = "https://api.balldontlie.io/v1/games"
BALLEDONTLIE_API_KEY = os.getenv("BALLEDONTLIE_API_KEY")


def get_schedule():
    """
    Fetch today's NBA games from balldontlie.
    Returns:
        - schedule: list of "Visitor vs Home" strings
        - teams_playing: set of team full names
    """
    today = date.today().isoformat()
    params = {"dates[]": today}
    headers = {"Authorization": f"Bearer {BALLEDONTLIE_API_KEY}"} if BALLEDONTLIE_API_KEY else {}

    try:
        response = requests.get(BALLEDONTLIE_GAMES_URL, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json().get("data", [])
        schedule = []
        teams_playing = set()
        for g in data:
            home = g["home_team"]["full_name"]
            visitor = g["visitor_team"]["full_name"]
            schedule.append(f"{visitor} vs {home}")
            teams_playing.update([home, visitor])
        return schedule, teams_playing
    except requests.RequestException as e:
        print(f"Failed to fetch schedule: {e}")
        return [f"Failed to fetch schedule: {e}"], set()


def daily_report():
    """
    Generate the daily NBA report for Discord.
    Includes:
        - Schedule
        - Injuries (only for teams playing today)
    Returns:
        String (max ~1900 chars for Discord)
    """
    now = datetime.now()
    report = f"🏀 **NBA Daily Report** 🏀\n_Time: {now.strftime('%Y-%m-%d %H:%M:%S')}_\n\n"

    # Schedule
    schedule, teams_playing = get_schedule()
    report += "**Today's Schedule:**\n"
    if schedule:
        for game in schedule:
            report += f"• {game}\n"
    else:
        report += "No games scheduled today\n"
    report += "\n"

    # Injuries
    all_injuries = get_injuries()
    report += "**Injury Report:**\n"
    any_injury = False
    for team in teams_playing:
        if team in all_injuries and all_injuries[team]:
            report += f"**{team}**\n"
            for p in all_injuries[team]:
                report += f" - {p['player']} ({p['status']}): {p['note']}\n"
            report += "\n"
            any_injury = True

    if not any_injury:
        report += "No injury data available today.\n"

    return report[:1900]


def picks_report():
    """
    Generate a simple picks report placeholder.
    Returns:
        String for Discord
    """
    now = datetime.now()
    return f"🏀 **NBA Daily Picks** 🏀\n_Time: {now.strftime('%Y-%m-%d %H:%M:%S')}_\n\nSchedule + injuries enabled.\n"


# -----------------------------
# Test locally
# -----------------------------
if __name__ == "__main__":
    print(daily_report())
    print("\n\n")
    print(picks_report())
