from datetime import date
from src.fetch_schedule import get_todays_games
from src.fetch_injuries import get_injuries

# Mapping to match NBA.com team names to ESPN names (adjust as needed)
TEAM_NAME_MAP = {
    "Golden State Warriors": "Golden State",
    "Los Angeles Lakers": "Los Angeles Lakers",
    "Boston Celtics": "Boston Celtics",
    "New York Knicks": "New York Knicks",
    "Miami Heat": "Miami",
    "Chicago Bulls": "Chicago",
    # Add all NBA teams here for full mapping
}

def picks_report():
    """
    Placeholder picks report.
    Will be replaced later with real statistical picks.
    """
    today = date.today().strftime("%B %d, %Y")
    return f"""
🏀 **Top NBA Picks — {today}**

1. Placeholder Pick — 60%
2. Placeholder Pick — 58%
3. Placeholder Pick — 55%

(Automation test successful)
"""

def daily_report():
    """
    Fetches today's NBA games and formats a daily report.
    Includes injuries under each matchup.
    """
    today = date.today().strftime("%B %d, %Y")
    games = get_todays_games()
    injuries = get_injuries()

    report = f"🏀 **NBA Daily Report — {today}**\n\n"

    if not games:
        report += "No games today.\n"
        return report

    for game in games:
        report += f"• {game}\n"

        try:
            home, away = game.split(" @ ")
        except ValueError:
            home, away = game, ""

        for team in [away, home]:
            espn_team = TEAM_NAME_MAP.get(team, team)  # Map to ESPN name
            if espn_team in injuries and injuries[espn_team]:
                report += f"  {team} Injuries:\n"
                for p in injuries[espn_team]:
                    report += f"    - {p['player']} ({p['position']}) — {p['status']}\n"

    return report

# -------------------------
# TEST DAILY REPORT
# -------------------------
if __name__ == "__main__":
    print("=== PICKS REPORT ===")
    print(picks_report())
    print("\n=== DAILY REPORT ===")
    print(daily_report())
