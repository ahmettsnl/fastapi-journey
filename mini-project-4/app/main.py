from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, List
import uuid

app = FastAPI()


# -----------------------------
# DATA STORAGE
# -----------------------------
polls: Dict[str, dict] = {}


# -----------------------------
# MODELS
# -----------------------------
class PollCreate(BaseModel):
    question: str
    options: List[str]


class VoteRequest(BaseModel):
    option: str


# -----------------------------
# CONNECTION MANAGER
# -----------------------------
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, poll_id: str, websocket: WebSocket):
        await websocket.accept()

        if poll_id not in self.active_connections:
            self.active_connections[poll_id] = []

        self.active_connections[poll_id].append(websocket)

    def disconnect(self, poll_id: str, websocket: WebSocket):
        if poll_id in self.active_connections:
            if websocket in self.active_connections[poll_id]:
                self.active_connections[poll_id].remove(websocket)

    async def broadcast(self, poll_id: str, data: dict):
        if poll_id in self.active_connections:
            disconnected_clients = []

            for connection in self.active_connections[poll_id]:
                try:
                    await connection.send_json(data)
                except:
                    disconnected_clients.append(connection)

            for dc in disconnected_clients:
                self.active_connections[poll_id].remove(dc)


manager = ConnectionManager()


# -----------------------------
# REST API
# -----------------------------
@app.post("/polls")
def create_poll(poll: PollCreate):
    poll_id = str(uuid.uuid4())

    polls[poll_id] = {
        "id": poll_id,
        "question": poll.question,
        "votes": {option: 0 for option in poll.options}
    }

    return polls[poll_id]


@app.get("/polls")
def get_polls():
    return list(polls.values())


@app.get("/polls/{poll_id}")
def get_poll(poll_id: str):
    if poll_id not in polls:
        return {"error": "Poll not found"}

    return polls[poll_id]


@app.post("/polls/{poll_id}/vote")
async def vote_rest(poll_id: str, vote: VoteRequest):
    if poll_id not in polls:
        return {"error": "Poll not found"}

    if vote.option not in polls[poll_id]["votes"]:
        return {"error": "Invalid option"}

    polls[poll_id]["votes"][vote.option] += 1

    await manager.broadcast(poll_id, polls[poll_id])

    return polls[poll_id]


@app.delete("/polls/{poll_id}")
def delete_poll(poll_id: str):
    if poll_id not in polls:
        return {"error": "Poll not found"}

    deleted = polls.pop(poll_id)

    return {
        "message": "Poll deleted",
        "poll": deleted
    }


# -----------------------------
# WEBSOCKET
# -----------------------------
@app.websocket("/ws/polls/{poll_id}")
async def websocket_endpoint(websocket: WebSocket, poll_id: str):
    await manager.connect(poll_id, websocket)

    try:
        if poll_id in polls:
            await websocket.send_json(polls[poll_id])

        while True:
            data = await websocket.receive_json()

            option = data.get("option")

            if (
                poll_id in polls
                and option in polls[poll_id]["votes"]
            ):
                polls[poll_id]["votes"][option] += 1

                await manager.broadcast(
                    poll_id,
                    polls[poll_id]
                )

    except WebSocketDisconnect:
        manager.disconnect(poll_id, websocket)


# -----------------------------
# SIMPLE TEST UI
# -----------------------------
@app.get("/")
def home():
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Real-Time Poll</title>
</head>
<body>

    <h1>Real-Time Polling App</h1>

    <button onclick="createPoll()">Create Poll</button>

    <h2 id="question"></h2>

    <div id="buttons"></div>

    <h3>Live Results</h3>

    <ul id="results"></ul>

    <script>

        let socket = null
        let currentPollId = null

        const params = new URLSearchParams(window.location.search)
        const pollIdFromUrl = params.get("poll")

        async function createPoll() {

            const response = await fetch('/polls', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    question: 'Best Programming Language?',
                    options: ['Python', 'JavaScript', 'Java']
                })
            })

            const poll = await response.json()

            window.location.href = `/?poll=${poll.id}`
        }

        function connectWebSocket(pollId) {

            currentPollId = pollId

            socket = new WebSocket(
                `ws://127.0.0.1:8000/ws/polls/${pollId}`
            )

            socket.onmessage = function(event) {

                const data = JSON.parse(event.data)

                document.getElementById("question").innerText =
                    data.question

                const buttonsDiv =
                    document.getElementById("buttons")

                buttonsDiv.innerHTML = ""

                Object.keys(data.votes).forEach(option => {

                    const btn =
                        document.createElement("button")

                    btn.innerText = option

                    btn.onclick = () => {

                        socket.send(
                            JSON.stringify({
                                option: option
                            })
                        )
                    }

                    buttonsDiv.appendChild(btn)
                })

                const results =
                    document.getElementById("results")

                results.innerHTML = ""

                Object.entries(data.votes).forEach(([key, value]) => {

                    const li =
                        document.createElement("li")

                    li.innerText = `${key}: ${value}`

                    results.appendChild(li)
                })
            }
        }

        if (pollIdFromUrl) {
            connectWebSocket(pollIdFromUrl)
        }

    </script>

</body>
</html>
"""

    return HTMLResponse(content=html_content)