from src.report_writer import picks_report, daily_report
from src.send_discord import send  # your existing Discord webhook sender

PICKS_WEBHOOK = "https://discord.com/api/webhooks/1451285690158546965/mJnVnJ8GDmkWFcU8S-nHoSyJL0aWSri-erfqw-3pekFy5LOZek0QK7pXF65DdHucspn1"
REPORT_WEBHOOK = "https://discord.com/api/webhooks/1451299023335063562/7M3u4hJ_vaJ0Q8LweCojTvX2halUGJAGrUE1Wv1LMb28Fwb3wB7mkuJOMAuw6nThmKKA"

# Send top picks
send(PICKS_WEBHOOK, picks_report())

# Send daily report
send(REPORT_WEBHOOK, daily_report())
