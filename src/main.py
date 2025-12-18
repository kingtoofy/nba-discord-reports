# src/main.py

import os
import requests
from src.report_writer import daily_report, picks_report

DAILY_REPORT_WEBHOOK = os.getenv("DISCORD_DAILY_WEBHOOK")
TOP_PICKS_WEBHOOK = os.getenv("DISCORD_PICKS_WEBHOOK")

def send_discord(webhook_url, message):
    if not webhook_url:
        print("Webhook URL not set!")
        return
    if not message.strip():
        print("Message is empty! Nothing to send.")
        return

    payload = {"content": message}
    print(f"Sending to webhook: {webhook_url[:30]}...")  # debug
    try:
        r = requests.post(webhook_url, json=payload)
        print(f"Discord response status: {r.status_code}")
        print(f"Discord response text: {r.text}")
        if r.status_code != 204 and r.status_code != 200:
            print(f"Failed to send Discord message: {r.status_code} {r.text}")
        else:
            print("Discord message sent successfully!")
    except Exception as e:
        print(f"Error sending Discord message: {e}")

def main():
    daily_msg = daily_report()
    send_discord(DAILY_REPORT_WEBHOOK, daily_msg)

    picks_msg = picks_report()
    send_discord(TOP_PICKS_WEBHOOK, picks_msg)

if __name__ == "__main__":
    main()
