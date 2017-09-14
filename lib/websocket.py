
import asyncio
import websockets

from .chatango.constants import ORIGIN

class WebSocket(object):
    def __init__(self, ws_uri, controller):
        self.controller = controller
        self.ws_uri = ws_uri
        self.connected = False
        self.__websocket = None

    async def start(self):
        async with websockets.connect(self.ws_uri, origin=ORIGIN) as websocket:
            self.connected = True
            self.__websocket = websocket
            await self.controller.websocket_opened()
            while self.connected:
                try:
                    ws_frame = await websocket.recv()
                    asyncio.ensure_future(
                        self.controller.handle_frame(
                            ws_frame.replace("\r\n", "").replace("\x00", "")))
                except websockets.exceptions.ConnectionClosed:
                    await self.stop()

    async def send(self, frame):
        try:
            await self.__websocket.send(frame)
        except websockets.exceptions.ConnectionClosed:
            await self.stop()

    async def stop(self):
        await self.__websocket.close()
