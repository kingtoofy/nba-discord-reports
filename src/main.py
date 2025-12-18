import os
import requests
from src.report_writer import daily_report, picks_report

DAILY_WEBHOOK = os.getenv("DISCORD_DAILY_WEBHOOK")
PICKS_WEBHOOK = os.getenv("DISCORD_PICKS_WEBHOOK")

def send(webhook, content):
    """
    Send a message to a Discord webhook with basic error handling.
    """
    try:
        response = requests.post(webhook, json={"content": content}, timeout=10)
        response.raise_for_status()
        print("Message sent successfully.")
    except requests.RequestException as e:
        print(f"Failed to send Discord message: {e}")

def main():
    # Daily report
    try:
        daily_msg = daily_report()
    except Exception as e:
        daily_msg = f"⚠️ Failed to generate daily report: {e}"
    send(DAILY_WEBHOOK, daily_msg)

    # Picks report
    try:
        picks_msg = picks_report()
    except Exception as e:
        picks_msg = f"⚠️ Failed to generate picks report: {e}"
    send(PICKS_WEBHOOK, picks_msg)

if __name__ == "__main__":
    main()
