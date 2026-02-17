// ClipSync Server - WebSocket Relay
// Deploy this on Railway, Render, or Glitch (all free)

const WebSocket = require('ws');
const http = require('http');

const PORT = process.env.PORT || 8080;

const server = http.createServer((req, res) => {
  if (req.url === '/health') {
    res.writeHead(200);
    res.end('ClipSync Server Running ✓');
  } else {
    res.writeHead(200);
    res.end('ClipSync WebSocket Server');
  }
});

const wss = new WebSocket.Server({ server });

// rooms: { roomCode: Set<ws> }
const rooms = new Map();

function getRoomCode(ws) {
  for (const [code, clients] of rooms.entries()) {
    if (clients.has(ws)) return code;
  }
  return null;
}

wss.on('connection', (ws) => {
  console.log('New connection');

  ws.on('message', (data) => {
    let msg;
    try {
      msg = JSON.parse(data);
    } catch {
      return;
    }

    const { type, room, payload } = msg;

    if (type === 'join') {
      // Leave any existing room
      const oldRoom = getRoomCode(ws);
      if (oldRoom) {
        rooms.get(oldRoom).delete(ws);
        if (rooms.get(oldRoom).size === 0) rooms.delete(oldRoom);
      }

      // Join new room
      if (!rooms.has(room)) rooms.set(room, new Set());
      rooms.get(room).add(ws);

      const count = rooms.get(room).size;
      ws.send(JSON.stringify({ type: 'joined', room, devices: count }));

      // Notify others in room
      rooms.get(room).forEach((client) => {
        if (client !== ws && client.readyState === WebSocket.OPEN) {
          client.send(JSON.stringify({ type: 'device_joined', devices: count }));
        }
      });

      console.log(`Room ${room}: ${count} device(s)`);
    }

    if (type === 'clipboard') {
      const currentRoom = getRoomCode(ws);
      if (!currentRoom) return;

      // Broadcast to all OTHER devices in the room
      rooms.get(currentRoom).forEach((client) => {
        if (client !== ws && client.readyState === WebSocket.OPEN) {
          client.send(JSON.stringify({ type: 'clipboard', payload, from: msg.from }));
        }
      });

      console.log(`Clipboard sync in room ${currentRoom}: ${String(payload).substring(0, 50)}...`);
    }

    if (type === 'ping') {
      ws.send(JSON.stringify({ type: 'pong' }));
    }
  });

  ws.on('close', () => {
    const room = getRoomCode(ws);
    if (room && rooms.has(room)) {
      rooms.get(room).delete(ws);
      const count = rooms.get(room).size;
      if (count === 0) {
        rooms.delete(room);
      } else {
        rooms.get(room).forEach((client) => {
          if (client.readyState === WebSocket.OPEN) {
            client.send(JSON.stringify({ type: 'device_left', devices: count }));
          }
        });
      }
      console.log(`Room ${room}: ${count} device(s) remaining`);
    }
    console.log('Connection closed');
  });

  ws.on('error', (err) => console.error('WS error:', err.message));
});

server.listen(PORT, () => {
  console.log(`ClipSync server running on port ${PORT}`);
});
