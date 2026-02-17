# 📋 ClipSync — Real-Time Clipboard Sync
### Phone ↔ Laptop over the Internet (No BT/WiFi needed)

---

## Features
- **Works Anywhere**: Syncs over the internet (4G/5G/WiFi), not just local network.
- **Native Experience**: Installable mobile app (PWA) with auto-send.
- **Easy Setup**: Zero-config desktop app with auto-tunneling (ngrok).
- **Secure**: Uses unique Room Codes and encrypted connections.

---

## 🚀 Quick Start in 2 Minutes

### 1. Run the Desktop App (Windows)
1. **Install Python** if you haven't.
2. Open a terminal in this folder and run:
   ```bash
   pip install websocket-client pyperclip pystray pillow pyngrok
   py clipsync_desktop.py
   ```
3. A **📋 clipboard icon** will appear in your system tray.
4. It will automatically:
   - Start the local server.
   - Create a secure tunnel (ngrok).
   - Show your **Room Code** (Right-click tray icon).

### 2. Install the Mobile App
1. On your phone, go to:
   👉 **[https://karthikondagurla.github.io/clipboard-sync/mobile.html](https://karthikondagurla.github.io/clipboard-sync/mobile.html)**
2. Tap the **Three Dots** (Chrome) or **Share** (Safari) -> **"Add to Home Screen"** or **"Install App"**.
3. Launch the new **ClipSync** app from your home screen.

### 3. Connect & Sync!
1. Open the mobile app.
2. Enter the **Room Code** shown on your laptop.
3. Tap **Connect**.
4. **Copy text** on either device — it appears on the other!

> **Note:** On mobile, privacy rules prevent background reading. To send from Phone -> Laptop:
> Copy text in another app, then **switch to ClipSync**. It will auto-paste and send!

---

## 🔧 Troubleshooting

**"Ngrok authentication failed"**
- The app should open a browser window for you to login to ngrok (free).
- Just copy your Authtoken from the dashboard and paste it into the app popup.

**"Connection failed" on phone**
- Ensure your phone has internet.
- Ensure the **Server URL** on phone matches the one in global config (check laptop terminal).
- If using the hosted version (Railway), mobile carriers might block it. Use the desktop app (ngrok) method instead.

**Phone not sending to Laptop**
- Mobile browsers block background clipboard access.
- You must **open the ClipSync app** to triggers the send.
- Ensure you tap "Allow" if the browser asks for clipboard permission.

---

## 📂 Files
| File | Purpose |
|------|---------|
| `clipsync_desktop.py` | Main Windows app. Runs server + tunnel + sync logic. |
| `server.js` | WebSocket relay server (runs locally via Python script). |
| `mobile.html` | The mobile app logic (PWA). |
| `manifest.json` | PWA metadata for "Add to Home Screen". |

---

*ClipSync — Built with WebSockets + Python + Vanilla HTML*
