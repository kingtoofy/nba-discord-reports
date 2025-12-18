# src/main.py

import os
import requests
from src.report_writer import daily_report, picks_report

# -----------------------------
# Discord webhook URLs
# Replace these with your actual webhook URLs
# -----------------------------
DAILY_REPORT_WEBHOOK = os.getenv("DAILY_REPORT_WEBHOOK")
TOP_PICKS_WEBHOOK = os.getenv("TOP_PICKS_WEBHOOK")

# -----------------------------
# Function to send message to Discord
# -----------------------------
def send_discord(webhook_url, message):
    if not webhook_url:
        print("Webhook URL not set!")
        return
    payload = {
        "content": message
    }
    try:
        r = requests.post(webhook_url, json=payload)
        if r.status_code != 204 and r.status_code != 200:
            print(f"Failed to send Discord message: {r.status_code} {r.text}")
        else:
            print("Discord message sent successfully!")
    except Exception as e:
        print(f"Error sending Discord message: {e}")

# -----------------------------
# Main function
# -----------------------------
def main():
    # 1. Daily report (schedule + injuries)
    daily_msg = daily_report()
    send_discord(DAILY_REPORT_WEBHOOK, daily_msg)

    # 2. Top picks report
    picks_msg = picks_report()
    send_discord(TOP_PICKS_WEBHOOK, picks_msg)

# -----------------------------
# Entry point
# -----------------------------
if __name__ == "__main__":
    main()
