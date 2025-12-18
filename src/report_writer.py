# src/report_writer.py

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from src.fetch_injuries import get_injuries

SCHEDULE_URL = "https://www.espn.com/nba/schedule"

def get_schedule():
    """
    Fetch today's NBA schedule from ESPN.
    Returns a list of matchups like ["LAL vs BOS", ...]
    """
    schedule = []
    try:
        response = requests.get(SCHEDULE_URL, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the main table with today's games
        schedule_table = soup.find("table", class_="Table")
        if schedule_table:
            rows = schedule_table.find_all("tr")[1:]  # skip header
            for row in rows:
                cells = row.find_all("td")
                if len(cells) >= 2:
                    team1 = cells[0].get_text(strip=True)
                    team2 = cells[1].get_text(strip=True)
                    schedule.append(f"{team1} vs {team2}")
    except Exception as e:
        schedule.append(f"Failed to fetch schedule: {e}")

    return schedule

def daily_report():
    """
    Generate the full daily report for Discord.
    Includes schedule + injury report.
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

    # Truncate to avoid Discord 2000 character limit
    return report[:1900]

def picks_report():
    """
    Dummy top picks report — replace with your AI/analysis logic.
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
