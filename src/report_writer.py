import os
import requests
from datetime import date, datetime

BALLEDONTLIE_GAMES_URL = "https://api.balldontlie.io/v1/games"
API_KEY = os.getenv("BALLEDONTLIE_API_KEY")

def get_schedule():
    today = date.today().isoformat()
    params = {"dates[]": today}

    headers = {
        "Authorization": f"Bearer {API_KEY}"
    }

    response = requests.get(
        BALLEDONTLIE_GAMES_URL,
        params=params,
        headers=headers,
        timeout=15
    )

    response.raise_for_status()

    games = response.json().get("data", [])
    schedule = []

    for g in games:
        away = g["visitor_team"]["full_name"]
        home = g["home_team"]["full_name"]
        schedule.append(f"{away} vs {home}")

    return schedule

def daily_report():
    now = datetime.now()
    msg = (
        "🏀 **NBA Daily Report** 🏀\n"
        f"_Generated: {now.strftime('%Y-%m-%d %H:%M:%S')}_\n\n"
        "**Today's Schedule:**\n"
    )

    schedule = get_schedule()

    if not schedule:
        msg += "No games scheduled today.\n"
    else:
        for game in schedule:
            msg += f"• {game}\n"

    return msg[:1900]

def picks_report():
    now = datetime.now()
    return (
        "🏀 **NBA Daily Picks** 🏀\n"
        f"_Generated: {now.strftime('%Y-%m-%d %H:%M:%S')}_\n\n"
        "Schedule-only mode active.\n"
    )
