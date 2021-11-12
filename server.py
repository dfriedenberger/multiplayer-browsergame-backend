import json

from fastapi import FastAPI, WebSocket , WebSocketDisconnect
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from fastapi_utils.tasks import repeat_every

from bomberman import Bomberman


app = FastAPI()
app.add_middleware(GZipMiddleware, minimum_size=500)



class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            message_str = json.dumps(message)
            await connection.send_text(message_str)




class Game:
    def __init__(self,id : str,connection_manager: ConnectionManager,game_handler):
        self.id = id
        self.connection_manager = connection_manager
        self.game_handler = game_handler

    def get_id(self):
        return self.id

    def get_connection_manager(self):
        return self.connection_manager

    async def recv(self,request):
        print("request",request)
        responses = self.game_handler.handle(request)
        print("responses",responses)
        for response in responses:
            await self.connection_manager.broadcast(response)




class GameManager:
    def __init__(self):
        self.games = dict()

    def get_games(self):
        return self.games.values()

    def get_game(self, game_type: str , game_id: str):
        id = "{0}/{1}".format(game_type,game_id)
        if id not in self.games:
            if game_type == "bomberman":
                self.games[id] = Game(id,ConnectionManager(),Bomberman())
            else: raise Exception("Unknown Game:"+game_type)
        return self.games[id]


gameManager = GameManager()

@app.on_event("startup")
@repeat_every(seconds=0.5)  # 1 hour
async def cycle() -> None:
    #print("cycle",len(gameManager.get_games()))
    for game in gameManager.get_games():
        await game.recv({"type" : "cycle" ,"cycle" : 500 })

@app.get("/")
async def get_root():
    return RedirectResponse("/assets/bomberman.html")

@app.websocket("/ws/{game_name}/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game_name: str , game_id: str):
    game = gameManager.get_game(game_name,game_id)
    await game.get_connection_manager().connect(websocket)
    try:
        while True:
            data_str = await websocket.receive_text()
            data = json.loads(data_str)
            await game.recv(data)
    except WebSocketDisconnect:
        game.get_connection_manager().disconnect(websocket)


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
