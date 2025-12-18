from datetime import date
from src.fetch_schedule import get_todays_games
from src.fetch_injuries import get_injuries

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
    Includes injuries from ESPN. Stats and odds will be added later.
    """
    today = date.today().strftime("%B %d, %Y")
    games = get_todays_games()
    injuries = get_injuries()

    if not games:
        return f"🏀 **NBA Daily Report — {today}**\n\nNo games today."

    report = f"🏀 **NBA Daily Report — {today}**\n\n"

    for game in games:
        report += f"• {game}\n"

        # Include injuries for both teams
        try:
            home, away = game.split(" @ ")
        except ValueError:
            home, away = game, ""
        for team in [away, home]:
            if team in injuries and injuries[team]:
                report += f"  {team} Injuries:\n"
                for p in injuries[team]:
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
