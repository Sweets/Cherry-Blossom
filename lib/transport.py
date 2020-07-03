
import asyncio

from .websocket import WebSocket

class Transport(object):
    """
    Transport
    Parent class for Room and PrivateMessages class
    Should *not* be used by an end-user.

    Parameters:
    - Instance of `Bot` (from cherryblossom.py) as `user`
    - Instance of `CherryBlossom` (from cherryblossom.py) as `controller`
    """
    def __init__(self, user, controller):
        self.user = user
        self.controller = controller
        self.websocket_server = None
        self.websocket = None

    async def join(self):
        if self.websocket_server:
            self.websocket = WebSocket(
                "wss://" + self.websocket_server + ":8081/", self)
            await self.websocket.start()

    async def leave(self):
        await self.websocket.stop()

    async def send_frame(self, *args, terminator="\r\n"):
        frame = [str(arg) for arg in args]
        await self.websocket.send(":".join(frame) + terminator)

    async def start_heartbeat(self):
        while self.websocket.connected:
            await asyncio.sleep(20)
            if self.websocket.connected:
                await self.send_frame("\r\n", terminator="\x00")

    async def split_frame(self, frame):
        frame_split = frame.split(":")
        command_name = frame_split[0]
        frame = frame_split[1:]
        return command_name, frame

    async def emit_event(self, event_name, *args):
        if hasattr(self.controller, event_name):
            asyncio.ensure_future(
                getattr(self.controller, event_name)(self, *args)
            )
