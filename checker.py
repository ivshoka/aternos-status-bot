import socket
import struct
import json
import requests
import os

HOSTNAME = "sigmalopolis.aternos.me"
PORT = 43065
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK")
STATUS_FILE = "status.json"


def mc_ping(host, port, timeout=5):
    """Perform Minecraft Server List Ping (SLP) to detect real server status."""

    try:
        ip = socket.getaddrinfo(host, port, socket.AF_INET)[0][4][0]
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((ip, port))

        # Send handshake packet
        data = b""
        data += b"\x00"                         # packet id = 0 (handshake)
        data += b"\x00"                         # protocol version
        data += struct.pack(">b", len(host))    # hostname length
        data += host.encode("utf-8")            # hostname
        data += struct.pack(">H", port)         # port
        data += b"\x01"                         # next state (status)
        packet = struct.pack(">b", len(data)) + data
        sock.send(packet)

        # Send request packet
        sock.send(b"\x01\x00")

        # Receive response
        _ = sock.recv(1024)
        sock.close()
        return True

    except Exception:
        return False


def send_discord(message):
    requests.post(WEBHOOK_URL, json={"content": message})


if os.path.exists(STATUS_FILE):
    with open(STATUS_FILE, "r") as f:
        last_status = json.load(f).get("status")
else:
    last_status = None


online = mc_ping(HOSTNAME, PORT)

if online and last_status != "online":
    send_discord(f"🟢 **Aternos Server is ONLINE!**\n`{HOSTNAME}:{PORT}`")
    current_status = "online"
elif not online and last_status != "offline":
    send_discord("🔴 **Aternos Server is OFFLINE.**")
    current_status = "offline"
else:
    current_status = last_status


with open(STATUS_FILE, "w") as f:
    json.dump({"status": current_status}, f)
