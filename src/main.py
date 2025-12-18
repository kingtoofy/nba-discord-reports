import os
from src.report_writer import picks_report, daily_report
from src.send_discord import send

PICKS_WEBHOOK = os.getenv("DISCORD_PICKS_WEBHOOK")
REPORT_WEBHOOK = os.getenv("DISCORD_REPORT_WEBHOOK")

send(PICKS_WEBHOOK, picks_report())
send(REPORT_WEBHOOK, daily_report())
