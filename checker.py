import socket
import time
import requests

HOSTNAME = "sigmalopolis.aternos.me"  # your Aternos hostname
PORT = 43065                          # your server port
WEBHOOK_URL = "https://discord.com/api/webhooks/1456854341800558675/C4nxyBartFND0TmYVHpBn3WNP36bpbRKFnFRQz-Sy7W1mRY_GAPeUcd9kCledfqj6cQv" # discord webhook

CHECK_INTERVAL = 60  # seconds

def is_port_open(ip, port):
    """Try connecting to the Minecraft server port."""
    try:
        sock = socket.create_connection((ip, port), timeout=4)
        sock.close()
        return True
    except:
        return False

def send_discord(message):
    """Send a message to Discord."""
    data = {"content": message}
    requests.post(WEBHOOK_URL, json=data)

def main():
    print("Starting Aternos monitor...")
    last_status = None

    while True:
        try:
            # Resolve IP each time in case Aternos changes it
            ip = socket.gethostbyname(HOSTNAME)

            online = is_port_open(ip, PORT)

            if online and last_status != "online":
                send_discord(f"🟢 **Server is ONLINE!**\n`{HOSTNAME}:{PORT}`")
                last_status = "online"

            elif not online and last_status != "offline":
                send_discord(f"🔴 **Server is OFFLINE.**")
                last_status = "offline"

        except Exception as e:
            print("Error:", e)

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
