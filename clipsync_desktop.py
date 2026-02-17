"""
ClipSync Desktop - Windows Clipboard Sync Client
Runs in system tray, syncs clipboard in real-time with your phone.

Install requirements:
    pip install websocket-client pyperclip pystray pillow

Run:
    python clipsync_desktop.py
"""

import threading
import time
import json
import random
import string
import sys
import os
import pyperclip
import websocket
import pystray
from PIL import Image, ImageDraw
from pystray import MenuItem as item

# ─── CONFIG ──────────────────────────────────────────────────────────────────
CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".clipsync_config.json")

def load_config():
    defaults = {
        "server": "wss://your-server.up.railway.app",
        "room": "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    }
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE) as f:
                saved = json.load(f)
                defaults.update(saved)
        except:
            pass
    return defaults

def save_config(cfg):
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)

config = load_config()
save_config(config)

# ─── STATE ───────────────────────────────────────────────────────────────────
ws_app = None
ws_conn = None
connected = False
last_sent = ""
tray_icon = None
status_text = "Disconnected"

# ─── WEBSOCKET ───────────────────────────────────────────────────────────────
def on_open(ws):
    global connected, status_text
    connected = True
    status_text = "Connected"
    ws.send(json.dumps({"type": "join", "room": config["room"]}))
    print(f"[ClipSync] Connected to room: {config['room']}")
    update_tray()

def on_message(ws, message):
    global last_sent
    try:
        msg = json.loads(message)
        mtype = msg.get("type")

        if mtype == "joined":
            devices = msg.get("devices", 1)
            print(f"[ClipSync] Room joined. {devices} device(s) connected.")
            update_status(f"Room: {config['room']} | {devices} device(s)")

        elif mtype in ("device_joined", "device_left"):
            devices = msg.get("devices", 1)
            label = "📱 Phone connected!" if mtype == "device_joined" else "📱 Device left"
            print(f"[ClipSync] {label} | {devices} device(s)")
            update_status(f"Room: {config['room']} | {devices} device(s)")

        elif mtype == "clipboard":
            payload = msg.get("payload", "")
            if payload and payload != last_sent:
                last_sent = payload
                pyperclip.copy(payload)
                print(f"[ClipSync] ← Received from phone: {payload[:60]}...")
                show_notification("ClipSync", f"📱 → 💻  Clipboard received!")

    except Exception as e:
        print(f"[ClipSync] Message error: {e}")

def on_close(ws, code, msg):
    global connected, status_text
    connected = False
    status_text = "Disconnected — reconnecting..."
    print("[ClipSync] Disconnected, will retry in 5s...")
    update_tray()

def on_error(ws, error):
    print(f"[ClipSync] WS Error: {error}")

def connect():
    global ws_app, ws_conn
    while True:
        try:
            ws_app = websocket.WebSocketApp(
                config["server"],
                on_open=on_open,
                on_message=on_message,
                on_close=on_close,
                on_error=on_error
            )
            ws_app.run_forever(ping_interval=30, ping_timeout=10)
        except Exception as e:
            print(f"[ClipSync] Connection failed: {e}")
        time.sleep(5)  # Wait before reconnecting

def send_clipboard(text):
    global last_sent, ws_app
    if ws_app and connected:
        last_sent = text
        try:
            ws_app.send(json.dumps({
                "type": "clipboard",
                "room": config["room"],
                "payload": text,
                "from": "laptop"
            }))
            print(f"[ClipSync] → Sent to phone: {text[:60]}...")
        except Exception as e:
            print(f"[ClipSync] Send error: {e}")

# ─── CLIPBOARD WATCHER ───────────────────────────────────────────────────────
def watch_clipboard():
    global last_sent
    last_clip = ""
    while True:
        try:
            current = pyperclip.paste()
            if current and current != last_clip and current != last_sent:
                last_clip = current
                if connected:
                    send_clipboard(current)
        except:
            pass
        time.sleep(0.5)  # Check every 500ms

# ─── SYSTEM TRAY ─────────────────────────────────────────────────────────────
def make_icon_image(color="#2563eb"):
    """Creates a simple clipboard icon for the tray"""
    img = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Clipboard body
    draw.rounded_rectangle([8, 12, 56, 60], radius=6, fill="#f4f4f1", outline=color, width=3)

    # Clip at top
    draw.rounded_rectangle([22, 6, 42, 18], radius=4, fill="#f4f4f1", outline=color, width=2)

    # Lines (text)
    r, g, b = int(color[1:3],16), int(color[3:5],16), int(color[5:7],16)
    line_color = (r, g, b, 160)
    draw.rectangle([16, 26, 48, 29], fill=line_color)
    draw.rectangle([16, 34, 42, 37], fill=line_color)
    draw.rectangle([16, 42, 38, 45], fill=line_color)

    return img

def update_status(text):
    global status_text
    status_text = text
    update_tray()

def update_tray():
    global tray_icon
    if tray_icon:
        color = "#2563eb" if connected else "#dc2626"
        tray_icon.icon = make_icon_image(color)
        tray_icon.title = f"ClipSync — {status_text}"

def show_notification(title, msg):
    """Show a Windows toast notification"""
    try:
        if tray_icon:
            tray_icon.notify(msg, title)
    except:
        pass

def open_room_info():
    import tkinter as tk
    from tkinter import messagebox, simpledialog

    root = tk.Tk()
    root.withdraw()

    info = (
        f"Your Room Code: {config['room']}\n\n"
        f"Server: {config['server']}\n\n"
        f"Open mobile.html on your phone and enter this room code.\n\n"
        f"Status: {'✓ Connected' if connected else '✗ Disconnected'}"
    )
    messagebox.showinfo("ClipSync Info", info)
    root.destroy()

def change_room():
    import tkinter as tk
    from tkinter import simpledialog

    root = tk.Tk()
    root.withdraw()

    new_room = simpledialog.askstring(
        "Change Room",
        f"Current room: {config['room']}\nEnter new room code (4-8 chars):",
        initialvalue=config["room"]
    )
    root.destroy()

    if new_room and len(new_room) >= 4:
        config["room"] = new_room.upper().strip()
        save_config(config)
        if ws_app and connected:
            ws_app.send(json.dumps({"type": "join", "room": config["room"]}))
        print(f"[ClipSync] Switched to room: {config['room']}")

def change_server():
    import tkinter as tk
    from tkinter import simpledialog

    root = tk.Tk()
    root.withdraw()

    new_server = simpledialog.askstring(
        "Change Server",
        "Enter WebSocket server URL:",
        initialvalue=config["server"]
    )
    root.destroy()

    if new_server:
        config["server"] = new_server.strip()
        save_config(config)
        print(f"[ClipSync] Server changed to: {config['server']}, reconnecting...")
        if ws_app:
            ws_app.close()

def quit_app(icon, item):
    icon.stop()
    os._exit(0)

def setup_tray():
    global tray_icon

    icon_img = make_icon_image("#aaaaaa")
    menu = pystray.Menu(
        item("📋 ClipSync", lambda: None, enabled=False),
        pystray.Menu.SEPARATOR,
        item(lambda text: f"Room: {config['room']} ({'●' if connected else '○'})", open_room_info),
        item("Change Room Code", change_room),
        item("Change Server URL", change_server),
        pystray.Menu.SEPARATOR,
        item("Quit", quit_app)
    )

    tray_icon = pystray.Icon(
        "ClipSync",
        icon_img,
        f"ClipSync — {status_text}",
        menu
    )

    return tray_icon

# ─── MAIN ────────────────────────────────────────────────────────────────────
def main():
    print("=" * 50)
    print("  ClipSync Desktop v1.0")
    print(f"  Room: {config['room']}")
    print(f"  Server: {config['server']}")
    print("  Running in system tray...")
    print("=" * 50)

    # Start WebSocket connection thread
    ws_thread = threading.Thread(target=connect, daemon=True)
    ws_thread.start()

    # Start clipboard watcher thread
    clip_thread = threading.Thread(target=watch_clipboard, daemon=True)
    clip_thread.start()

    # Run tray icon (blocks main thread)
    tray = setup_tray()
    tray.run()

if __name__ == "__main__":
    main()
