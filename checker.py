import socket
import requests
import json
import os

HOSTNAME = "sigmalopolis.aternos.me"
PORT = 43065
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")

STATUS_FILE = "status.json"

def resolve_ipv4(hostname):
    """Resolve hostname to IPv4 only (fixes GitHub Actions IPv6 issue)."""
    return socket.getaddrinfo(hostname, None, socket.AF_INET)[0][4][0]

def is_port_open(ip, port):
    try:
        sock = socket.create_connection((ip, port), timeout=4)
        sock.close()
        return True
    except:
        return False

def send_discord(message):
    requests.post(WEBHOOK_URL, json={"content": message})

# Load last status
if os.path.exists(STATUS_FILE):
    with open(STATUS_FILE, "r") as f:
        last_status = json.load(f).get("status")
else:
    last_status = None

# RESOLVE IP USING IPv4 ONLY
ip = resolve_ipv4(HOSTNAME)

online = is_port_open(ip, PORT)

if online and last_status != "online":
    send_discord(f"🟢 **Aternos Server is ONLINE!**\n`{HOSTNAME}:{PORT}`")
    current_status = "online"

elif not online and last_status != "offline":
    send_discord("🔴 **Aternos Server is OFFLINE.**")
    current_status = "offline"

else:
    current_status = last_status

# Save status
with open(STATUS_FILE, "w") as f:
    json.dump({"status": current_status}, f)
