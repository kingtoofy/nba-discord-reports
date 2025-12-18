# src/report_writer.py

import requests
from bs4 import BeautifulSoup

# -----------------------------
# Configuration
# -----------------------------
SCHEDULE_URL = "https://www.espn.com/nba/schedule"
SPORTSETHOS_URL = "https://sportsethos.com/live-injury-report/"

# -----------------------------
# Fetch today's NBA schedule
# -----------------------------
def get_schedule():
    schedule = []
    try:
        response = requests.get(SCHEDULE_URL, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Each game block (adjust selectors based on ESPN HTML)
        game_containers = soup.select("table tbody tr")
        for game in game_containers:
            cells = game.find_all("td")
            if len(cells) < 2:
                continue
            team1 = cells[0].get_text(strip=True)
            team2 = cells[1].get_text(strip=True)
            schedule.append(f"{team1} vs {team2}")
    except Exception as e:
        schedule.append(f"Failed to fetch schedule: {e}")
    return schedule

# -----------------------------
# Fetch today's NBA injuries from Sportsethos
# -----------------------------
def get_injuries():
    injuries = {}
    try:
        response = requests.get(SPORTSETHOS_URL, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Each team section is a div with class 'injury-team'
        team_sections = soup.select("div.injury-team")
        for team_div in team_sections:
            team_name_tag = team_div.find("h3")
            if not team_name_tag:
                continue
            team_name = team_name_tag.get_text(strip=True)
            injuries[team_name] = []

            player_rows = team_div.select("li")
            for row in player_rows:
                text = row.get_text(" ", strip=True)
                parts = text.split(" — ")
                note = parts[1] if len(parts) > 1 else ""
                player_status = parts[0].split()
                if len(player_status) < 3:
                    continue
                player_name = " ".join(player_status[:-2])
                position = player_status[-2]
                status = player_status[-1]
                injuries[team_name].append({
                    "player": player_name,
                    "position": position,
                    "status": status,
                    "note": note
                })
    except Exception as e:
        injuries["Error"] = [{"player": "", "position": "", "status": "Error", "note": str(e)}]

    return injuries

# -----------------------------
# Generate the daily Discord report
# -----------------------------
def daily_report():
    report = "🏀 **NBA Daily Report** 🏀\n\n"

    # 1. Schedule
    schedule = get_schedule()
    report += "**Today's Schedule:**\n"
    for game in schedule:
        report += f" - {game}\n"
    report += "\n"

    # 2. Injuries
    injuries = get_injuries()
    report += "**Injury Report:**\n"
    for team, players in injuries.items():
        report += f"**{team}**\n"
        if players:
            for p in players:
                report += f" - {p['player']} ({p['position']}) — {p['status']}: {p['note']}\n"
        else:
            report += " - No injuries reported\n"
        report += "\n"

    return report

# -----------------------------
# Generate the top picks report
# (dummy example, can replace with real prop logic)
# -----------------------------
def picks_report():
    report = "🏀 **NBA Top Picks of the Day** 🏀\n\n"
    # Replace the example picks with your real analysis
    top_picks = [
        {"player": "Trae Young", "pick": "Over 28.5 P+R+A", "confidence": "92%"},
        {"player": "Jayson Tatum", "pick": "Under 30.5 P+R+A", "confidence": "88%"},
        {"player": "LeBron James", "pick": "Over 25.5 P", "confidence": "85%"},
    ]
    for pick in top_picks:
        report += f"{pick['player']} — {pick['pick']} (Confidence: {pick['confidence']})\n"
    return report

# -----------------------------
# Test run locally
# -----------------------------
if __name__ == "__main__":
    print(daily_report())
    print("\n\n")
    print(picks_report())
