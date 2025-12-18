from src.report_writer import picks_report, daily_report
from src.send_discord import send  # your existing Discord webhook sender

PICKS_WEBHOOK = "YOUR_WEBHOOK_URL_FOR_NBA_DAILY_PICKS"
REPORT_WEBHOOK = "YOUR_WEBHOOK_URL_FOR_NBA_DAILY_REPORT"

# Send top picks
send(PICKS_WEBHOOK, picks_report())

# Send daily report
send(REPORT_WEBHOOK, daily_report())
