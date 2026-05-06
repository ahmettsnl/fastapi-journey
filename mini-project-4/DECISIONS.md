# DECISIONS.md

## 1. Connection Management

I used a connection manager class to store all active WebSocket connections in a dictionary. Each poll ID has its own list of connected clients. When a user connects, their WebSocket is added to the list. When they disconnect, it is removed.

If a client disconnects while voting, the application does not crash because disconnected clients are removed safely from the active connections list. I used try/except handling during broadcasting to avoid server errors.

---

## 2. State Storage

I stored poll data and votes in memory using Python dictionaries because this project is small and focused on learning WebSockets and real-time communication.

The disadvantage is that all polls and votes are lost if the server restarts because nothing is saved permanently.

To make this production-ready, I would use a real database like PostgreSQL or MongoDB and save poll data there instead of memory.

---

## 3. Concurrency

If two users vote at the same exact moment, both requests are processed very quickly by FastAPI. In this small project, I did not implement advanced concurrency protection.

The risk is that in a very high traffic system, some vote updates could conflict or overwrite each other. In a real production system, database transactions or locks should be used.

---

## 4. REST vs WebSocket

The REST vote endpoint sends one request and receives one response. It works like normal API communication.

The WebSocket connection stays open continuously, so all connected clients receive updates instantly without refreshing the page.

REST is useful for simple API communication or fallback support. WebSocket is better for real-time applications where users need instant updates.