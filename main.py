import time
import requests
from mcstatus import JavaServer

WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL"

SERVER_ADDRESS = "sigmalopolis.aternos.me"
SERVER_PORT = 43065

was_online = False

def send_message(msg):
    requests.post(WEBHOOK_URL, json={"content": msg})

while True:
    try:
        server = JavaServer.lookup(f"{SERVER_ADDRESS}:{SERVER_PORT}")
        status = server.status()  # This pings the MC server

        if not was_online:
            send_message("🟢 **Aternos Server is ONLINE!**")
            was_online = True

    except Exception:
        if was_online:
            send_message("🔴 **Aternos Server is OFFLINE.**")
            was_online = False

    time.sleep(60)  # check every 60 seconds
