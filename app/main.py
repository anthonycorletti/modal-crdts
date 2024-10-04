import asyncio
import logging

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from ypy_websocket.websocket_server import WebsocketServer
from ypy_websocket.yroom import YRoom
from ypy_websocket.ystore import SQLiteYStore

from app.settings import settings

app = FastAPI()

logging.basicConfig(level=settings.LOG_LEVEL)
log = logging.getLogger(__name__)


class SQLiteYStoreWrapper(SQLiteYStore):
    db_path = settings.DB_PATH


class WebsocketServerWrapper(WebsocketServer):
    async def get_room(self, name: str) -> YRoom:
        if name not in self.rooms:
            ystore = SQLiteYStoreWrapper(path=f".{name}.y")
            self.rooms[name] = YRoom(ystore=ystore, log=log)
        room = self.rooms[name]
        await self.start_room(room)
        return room


app.mount("/static", StaticFiles(directory="app/static"), name="static")
ws_server = WebsocketServerWrapper(auto_clean_rooms=False, log=log)


@app.get("/", response_class=HTMLResponse)
async def _index() -> HTMLResponse:
    with open("app/static/index.html", "r") as f:
        content = f.read()
    return HTMLResponse(content)


@app.websocket("/ws/{room_name}")
async def websocket_endpoint(websocket: WebSocket, room_name: str) -> None:
    await websocket.accept()
    print("websocket accepted...")
    task = asyncio.create_task(ws_server.start())
    print("task created...")
    await ws_server.started.wait()
    print("server started...")
    try:
        print("serving websocket...")
        await asyncio.create_task(
            ws_server.serve(websocket=WebsocketAdapter(websocket, room_name))
        )
        print("websocket served...")
    except Exception:
        print("handing exception...")
        ws_server.stop()
        print("server stopped...")
        task.cancel()
        print("task cancelled...")


class WebsocketAdapter:
    def __init__(self, websocket: WebSocket, path: str) -> None:
        self._websocket = websocket
        self._path = path

    @property
    def path(self) -> str:
        return self._path

    @path.setter
    def path(self, value: str) -> None:
        self._path = value

    def __aiter__(self) -> "WebsocketAdapter":
        return self

    async def __anext__(self) -> bytes:
        try:
            message = await self._websocket.receive_bytes()
        except WebSocketDisconnect:
            raise StopAsyncIteration()
        return message

    async def send(self, message: bytes) -> None:
        await self._websocket.send_bytes(message)

    async def recv(self) -> bytes:
        message = await self._websocket.receive_bytes()
        return message
