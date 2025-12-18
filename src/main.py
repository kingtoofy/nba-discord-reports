import os
import requests
from src.report_writer import daily_report, picks_report

DAILY_WEBHOOK = os.getenv("DISCORD_DAILY_WEBHOOK")
PICKS_WEBHOOK = os.getenv("DISCORD_PICKS_WEBHOOK")

def send(webhook, content):
    requests.post(webhook, json={"content": content}, timeout=10)

def main():
    send(DAILY_WEBHOOK, daily_report())
    send(PICKS_WEBHOOK, picks_report())

if __name__ == "__main__":
    main()
