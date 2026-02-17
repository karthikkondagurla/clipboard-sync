# 📋 ClipSync — Real-Time Clipboard Sync
### Phone ↔ Laptop over the Internet (No BT/WiFi needed between devices)

---

## How It Works

```
Your Phone (Chrome)  ←──WebSocket──→  Server (Cloud)  ←──WebSocket──→  Your Laptop (Python)
```

Both devices connect to a free cloud server using a **Room Code**.
Anything copied on either device is instantly sent to the other.

---

## STEP 1 — Deploy the Server (Free, 5 minutes)

### Option A: Railway (Recommended — Completely Free)
1. Go to https://railway.app and sign up (free)
2. Click **"New Project" → "Deploy from GitHub repo"**
3. Or use **"Deploy from template"** → paste this as a new service
4. Upload `server.js` and `package.json`
5. Railway auto-detects Node.js and deploys
6. Copy your URL: `your-app.up.railway.app`
7. Your WebSocket URL will be: `wss://your-app.up.railway.app`

### Option B: Render (Also Free)
1. Go to https://render.com
2. New → Web Service → connect GitHub repo
3. Build command: `npm install`
4. Start command: `node server.js`
5. Copy the `onrender.com` URL → replace `https://` with `wss://`

### Option C: Glitch (Easiest)
1. Go to https://glitch.com
2. New Project → Hello Node.js
3. Replace `server.js` content with our `server.js`
4. Add `ws` to `package.json` dependencies
5. Your URL: `wss://your-project.glitch.me`

---

## STEP 2 — Set Up Windows Laptop

### Install Python dependencies:
```bash
pip install websocket-client pyperclip pystray pillow
```

### Edit the server URL in `clipsync_desktop.py`:
Open the file, find this line near the top:
```python
"server": "wss://your-server.up.railway.app"
```
Replace with your actual server URL from Step 1.

### Run:
```bash
python clipsync_desktop.py
```

A **📋 clipboard icon** appears in your system tray (bottom-right of Windows taskbar).
- **Right-click** the icon → see your Room Code
- The app runs in the background and auto-reconnects

### (Optional) Auto-start with Windows:
1. Press `Win + R`, type `shell:startup`
2. Create a shortcut to `clipsync_desktop.py` there
3. Or create a `.bat` file:
   ```bat
   @echo off
   pythonw clipsync_desktop.py
   ```

---

## STEP 3 — Set Up Phone (Android Chrome)

1. Open `mobile.html` in Chrome on your Android phone
   - Either host it somewhere, or open it directly from a shared file
   - Easiest: host on GitHub Pages for free
2. Tap the **⚙ server** dropdown → enter your server URL → Save
3. Enter your **Room Code** (same as laptop) → tap **Join**
4. Done! 🎉

---

## STEP 4 — Use It!

| Action | What Happens |
|--------|-------------|
| Copy text on laptop | Instantly appears on phone clipboard |
| Copy text on phone | Instantly appears on laptop clipboard |
| Room Code changes | Both devices disconnect from old room |
| Internet drops | Auto-reconnects when back online |

---

## Room Codes

- Your laptop generates a random room code on first run
- Saved in `~/.clipsync_config.json`
- You can change it anytime via the tray icon
- Share the same code on both devices
- Room codes are case-insensitive

---

## Troubleshooting

**"Connection failed" on laptop:**
- Check your server URL in `clipsync_desktop.py`
- Make sure the server is running (visit the HTTP URL in browser — should say "ClipSync WebSocket Server")
- Check your internet connection

**"Clipboard permission" error on phone:**
- In Chrome, tap the URL bar → lock icon → Permissions → allow Clipboard
- Or manually paste using the "Paste from Phone" button

**Phone auto-copy not working:**
- Chrome requires a user gesture for clipboard write
- Tap "Copy to Phone" button after receiving text

**Desktop app not in tray:**
- Check if Python is installed: `python --version`
- Install requirements: `pip install websocket-client pyperclip pystray pillow`
- Run from terminal to see error messages: `python clipsync_desktop.py`

---

## Files

| File | Purpose |
|------|---------|
| `server.js` | WebSocket relay server (deploy to cloud) |
| `package.json` | Node.js server dependencies |
| `mobile.html` | Android web app (open in Chrome) |
| `clipsync_desktop.py` | Windows background app (system tray) |
| `README.md` | This guide |

---

## Privacy

- Text passes through your server only — not stored anywhere
- Room codes are your only "password" — keep them private
- For extra security, deploy your own server (instructions above)
- No accounts, no signup, no tracking

---

*ClipSync — Built with WebSockets + Python + vanilla HTML*
