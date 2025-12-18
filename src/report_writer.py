from datetime import date

def picks_report():
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
    return f"""
🏀 **NBA Daily Report — {today}**

Games will appear here once data is wired.
"""
