from datetime import date
from src.fetch_schedule import get_todays_games
from src.fetch_injuries import get_injuries

# Complete mapping from NBA.com team names to ESPN injury names
TEAM_NAME_MAP = {
    "Atlanta Hawks": "Atlanta",
    "Boston Celtics": "Boston Celtics",
    "Brooklyn Nets": "Brooklyn",
    "Charlotte Hornets": "Charlotte",
    "Chicago Bulls": "Chicago",
    "Cleveland Cavaliers": "Cleveland",
    "Dallas Mavericks": "Dallas",
    "Denver Nuggets": "Denver",
    "Detroit Pistons": "Detroit",
    "Golden State Warriors": "Golden State",
    "Houston Rockets": "Houston",
    "Indiana Pacers": "Indiana",
    "Los Angeles Clippers": "LA Clippers",
    "Los Angeles Lakers": "Los Angeles Lakers",
    "Memphis Grizzlies": "Memphis",
    "Miami Heat": "Miami",
    "Milwaukee Bucks": "Milwaukee",
    "Minnesota Timberwolves": "Minnesota",
    "New Orleans Pelicans": "New Orleans",
    "New York Knicks": "New York Knicks",
    "Oklahoma City Thunder": "Oklahoma City",
    "Orlando Magic": "Orlando",
    "Philadelphia 76ers": "Philadelphia",
    "Phoenix Suns": "Phoenix",
    "Portland Trail Blazers": "Portland",
    "Sacramento Kings": "Sacramento",
    "San Antonio Spurs": "San Antonio",
    "Toronto Raptors": "Toronto",
    "Utah Jazz": "Utah",
    "Washington Wizards": "Washington",
}

def picks_report():
    """
    Placeholder top 15 picks report.
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
    Includes injuries for each team under the correct matchup.
    """
    today = date.today().strftime("%B %d, %Y")
    games = get_todays_games()
    injuries = get_injuries() or {}

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
            espn_team = TEAM_NAME_MAP.get(team, team)
            if espn_team in injuries and injuries[espn_team]:
                report += f"  {team} Injuries:\n"
                for p in injuries[espn_team]:
                    report += f"    - {p['player']} ({p['position']}) — {p['status']}\n"

    return report

# -------------------------
# TEST REPORTS
# -------------------------
if __name__ == "__main__":
    print("=== PICKS REPORT ===")
    print(picks_report())
    print("\n=== DAILY REPORT ===")
    print(daily_report())
