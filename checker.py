import socket
import requests
import json
import os

HOSTNAME = "sigmalopolis.aternos.me"
PORT = 43065
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")  # pulled from GitHub secrets

STATUS_FILE = "status.json"

def is_port_open(ip, port):
    try:
        sock = socket.create_connection((ip, port), timeout=4)
        sock.close()
        return True
    except:
        return False

def send_discord(message):
    data = {"content": message}
    requests.post(WEBHOOK_URL, json=data)

# Load last known status
if os.path.exists(STATUS_FILE):
    with open(STATUS_FILE, "r") as f:
        last_status = json.load(f).get("status")
else:
    last_status = None

# Resolve IP
ip = socket.gethostbyname(HOSTNAME)

# Check server status
online = is_port_open(ip, PORT)

if online and last_status != "online":
    send_discord(f"🟢 **Aternos Server is ONLINE!**\n`{HOSTNAME}:{PORT}`")
    current_status = "online"

elif not online and last_status != "offline":
    send_discord("🔴 **Aternos Server is OFFLINE.**")
    current_status = "offline"

else:
    current_status = last_status

# Save status for next run
with open(STATUS_FILE, "w") as f:
    json.dump({"status": current_status}, f)
