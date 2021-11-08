import json

from fastapi import FastAPI, WebSocket , WebSocketDisconnect
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.add_middleware(GZipMiddleware, minimum_size=500)

class ConnectionManager:
    def __init__(self):
        self.games = dict()
    
    def register(self, game: str , game_id: str):
        if game not in self.games:
            self.games[game] = dict()
        if game_id not in self.games[game]:
            self.games[game][game_id] = {
                "active_connections" : []
            }
    def unregister(self, game: str , game_id: str):
        if len(self.games[game][game_id]["active_connections"]) == 0:
            del self.games[game][game_id]
        if len(self.games[game].keys()) == 0:
            del self.games[game]

    async def connect(self, game: str , game_id: str,websocket: WebSocket):
        print("connect",game,game_id)
        await websocket.accept()       
        self.games[game][game_id]["active_connections"].append(websocket)

    def disconnect(self, game: str , game_id: str, websocket: WebSocket):
        print("disconnect",game,game_id)
        self.games[game][game_id]["active_connections"].remove(websocket)




    async def broadcast(self, game: str , game_id: str, message: str):
        for connection in self.games[game][game_id]["active_connections"]:
            await connection.send_text(json.dumps(message))


manager = ConnectionManager()


@app.get("/")
async def get_root():
    return RedirectResponse("/assets/bomberman.html")

@app.websocket("/ws/{game}/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game: str , game_id: str):
    manager.register(game,game_id)
    await manager.connect(game,game_id,websocket)
    client_id = None
    try:
        while True:
            data_str = await websocket.receive_text()
            data = json.loads(data_str)
            print("data",data)
            if "id" in data:
                client_id = data["id"]
            #Todo game engine
            await manager.broadcast(game,game_id,data)
    except WebSocketDisconnect:
        manager.disconnect(game,game_id,websocket)
        manager.unregister(game,game_id)
        await manager.broadcast(game,game_id,{"message" : "client left", "client_id" : client_id})



@app.get("/api/test", response_class=JSONResponse)
async def read_api_test():
    data = []
    
    data.append({
        "hello" : "world"
    })
    return data


# Register a regular HTTP route
@app.get("/trigger")
async def trigger_events():
    # Upon request trigger an event
    pubsubEndpoint.publish(["triggered"])
    return { "state" : "Ok" }







app.mount("/assets", StaticFiles(directory="assets"), name="assets")
