
"""
privatemessages.py
"""

import asyncio

from .eventhandlers import privatemessages as eventhandler
from .transport import Transport

class PrivateMessages(Transport):
    """
    Inherits from the Transport class
    """

    def __init__(self, user, controller):
        super().__init__(user, controller)
        self.websocket_server = "c1.chatango.com"

        self.friends = list()
        self.blocked = list()

    async def websocket_opened(self):
        await self.send_frame(
            "tlogin",
            self.user.get_auth_token(),
            2, self.user.user_id,
            terminator="\x00")
        asyncio.ensure_future(self.start_heartbeat())

    async def handle_frame(self, frame):
        command_name, frame = await super().split_frame(frame)
        if hasattr(eventhandler, command_name):
            if command_name == "time":
                command_name = "_time"
            asyncio.ensure_future(getattr(eventhandler, command_name)(self, *frame))
        else:
            if command_name != str():
                await self.emit_event("unmanaged_command", command_name, frame)

    # PMs is in need of a lot of work

    async def enable_background(self):
        await self.send_frame("getpremium")

    async def disable_background(self):
        await self.send_frame("msgbg", 0)

    async def send_message(self, *args, recipient=None):
        if isinstance(recipient, str): # verify username
            await self.send_frame("msg", recipient.lower(),
                                  "<n" + self.user.styles.name_color + "/><m v=\"1\"><g x" +
                                  self.user.styles.font_size + "s" +
                                  self.user.styles.font_color + "=\"" +
                                  self.user.styles.font_face + "\">" + " ".join(args) + "</g></m>"
                                 )
