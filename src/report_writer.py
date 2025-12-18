from datetime import date
from src.fetch_schedule import get_todays_games

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
    today = date.today().strftime("%B %d, %Y")
    games = get_todays_games()

    if not games:
        return f"🏀 **NBA Daily Report — {today}**\n\nNo games today."

    report = f"🏀 **NBA Daily Report — {today}**\n\n"

    for game in games:
        report += f"• {game}\n"

    return report
