
"""
privatemessages.py
"""

import asyncio

from sys import getsizeof

from .chatango.utilities import user_name_is_valid
from .chatango.constants import FONT_FACES, MAX_MESSAGE_SIZE
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

    async def get_friend(self, user_name):
        assert user_name_is_valid(user_name), "Invalid user name"
        for friend in self.friends:
            if friend.name == user_name.lower():
                return friend

    async def add_friend(self, user_name):
        assert user_name_is_valid(user_name), "Invalid user name"
        friend = await self.get_friend(user_name)
        if not friend:
            await self.send_frame("wladd", user_name.lower())

    async def remove_friend(self, user_name):
        assert user_name_is_valid(user_name), "Invalid user name"
        friend = await self.get_friend(user_name)
        if friend:
            await self.send_frame("wldelete", friend.name)

    async def send_message(self, *message, recipient=None):
        assert user_name_is_valid(recipient), "Invalid user name"
        
        if len(message) > 0:
            name_color = "<n{}/>".format(self.user.styles.name_color)
            
            font_size = self.user.styles.font_size if font_size > 10 else "09"
            font_face = self.user.styles.font_family
            font_face = FONT_FACES.get(font_face, font_face)
            
            message = "<br/>".join(message)
            
            message_xml = "<m v=\"1\"><g x{}s{}=\"{}\">{}</g></m>"
            format_parameters = (font_size,
                                 self.user.styles.font_color,
                                font_face,
                                message)
            
            message = name_color + message_xml.format(*format_parameters)
            
            if getsizeof(message) < MAX_MESSAGE_SIZE:
                await self.send_frame("msg", recipient.lower(), message)
