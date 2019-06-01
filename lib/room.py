
import asyncio

from .eventhandlers import room as eventhandler
from .chatango import flags
from .chatango.constants import FONT_FACES, MAX_MESSAGE_SIZE
from .chatango.utilities import get_room_server, user_name_is_valid
from .transport import Transport

class Room(Transport):
    def __init__(self, name, user, controller):
        super().__init__(user, controller)
        self.name = name
        self.websocket_server = get_room_server(name)

        self.owner = str()
        self.moderators = list()
        self.participants = list()
        self.banned_users = list()
        self.user_count = int()

        self.banned_words = {
            "exact": list(),
            "partial": list()}

        self.messages = dict()

    async def websocket_opened(self):
        await self.send_frame("v", terminator="\x00")
        await self.send_frame("bauth",
                              self.name,
                              self.user.user_id,
                              self.user.name,
                              self.user.get_password(),
                              terminator="\x00")
        asyncio.ensure_future(self.start_heartbeat())

    async def handle_frame(self, frame):
        command_name, frame = await super().split_frame(frame)
        if hasattr(eventhandler, command_name):
            asyncio.ensure_future(getattr(eventhandler, command_name)(self, *frame))
        else:
            if command_name != str():
                await self.emit_event("unmanaged_command", command_name, frame)

    async def get_participant(self, user_name, logged_in=True):
        # logged_in is specified in the event a temporary and an actual user
        # share a name. It can only happen under specific conditions:
        # The temporary user must be named before the user joins.

        # e.g. temp named bread is in the chat, then the user
        # that owns the bread account joins.
        # This is the only occassion when a temporary user
        # and a regular user may share a name.

        # Basically, logged_in should be False for temps and anons,
        # True otherwise
        assert user_name_is_valid(user_name), "User name is invalid"
        for participant in self.participants:
            if participant.name.lower() == user_name.lower() and participant.logged_in == logged_in:
                return participant

    async def enable_background(self):
        await self.send_frame("getpremium")

    async def disable_background(self):
        await self.send_frame("msgbg", 0)

    async def get_last_message(self, data, match="sender"):
        if match == "sender":
            assert user_name_is_valid(data), "User name is invalid"
            data = data.lower()
        for message in sorted(self.messages.values(), key=lambda msg: msg.time, reverse=True):
            if hasattr(message, match):
                if match == "sender":
                    if getattr(message, match).lower() == data:
                        return message
                else:
                    if getattr(message, match) == data:
                        return message
            else:
                return

    async def get_current_user(self):
        participant = await self.get_participant(self.user.name)
        if not isinstance(participant, type(None)):
            return participant

    async def current_user_is_moderator(self):
        current_user = await self.get_current_user()
        if current_user:
            if await current_user.is_moderator() or await current_user.is_administrator():
                return True
            return False
        return False

    async def get_block(self, user_name="", unique_id="", ip_address=""):
        assert user_name_is_valid(
            user_name), "User name is invalid"
        user_name = user_name.lower()
        assert await self.current_user_is_moderator(), "Current user is not a moderator"
        for ban_record in self.banned_users:
            if ban_record.user_name == user_name:
                return ban_record

    async def get_moderator(self, user_name):
        assert user_name_is_valid(user_name), "User name is invalid"
        user_name = user_name.lower()
        for moderator in self.moderators:
            if moderator.name == user_name:
                return moderator

    async def add_moderator(self, user_name, _flags=[]):
        assert user_name_is_valid(user_name), "User name is invalid"
        assert await self.current_user_is_moderator(), "Current user is not a moderator"
        current_user = await self.get_current_user()
        user_name = user_name.lower()

        if not await current_user.is_owner():
            if "edit_mods" not in self.moderators.get(current_user.name.lower()):
                return

        if not await self.get_moderator(user_name):
            packed_flags = 0
            for flag in _flags:
                if flag in flags.MODERATOR_FLAGS.keys():
                    flag = flags.MODERATOR_FLAGS.get(flag)
                    packed_flags = flags.pack_flag(packed_flags, flag)
            if packed_flags == 0:
                await self.add_moderator(user_name, _flags=flags.DEFAULT_MODERATOR_FLAGS)
            else:
                await self.send_frame("addmod", user_name, packed_flags)

    async def remove_moderator(self, user_name):
        assert user_name_is_valid(user_name), "User name is invalid"
        assert await self.current_user_is_moderator(), "Current user is not a moderator"
        current_user = await self.get_current_user()
        user_name = user_name.lower()

        if not await current_user.is_owner():
            if "edit_mods" not in self.moderators.get(current_user.name.lower()):
                return

        if await self.get_moderator(user_name):
            await self.send_frame("removemod", user_name)

    async def send_message(self, *message, _flags=[]):
        if len(message) > 0:
            packed_flags = 0
            for flag in _flags:
                flag = flags.MESSAGE_FLAGS.get(flag, -1)
                if flag > -1:
                    packed_flags = flags.pack_flag(packed_flags, flag)
            if self.user.name:
                name_color = "<n" + self.user.styles.name_color + "/>"
                
            font_size = self.user.styles.font_size if font_size > 10 else "09"
            
            font_face = self.user.styles.font_family
            font_face = FONT_FACES.get(font_face, font_face)
            
            message = name_color + "<f x{}{}=\"{}\">".format(
                str(font_size), self.user.styles.font_color,
                font_face) + "\r".join(message) + "</f>"
            
            # Spam-related checks should be performed here
            # MAX_MESSAGE_SIZE assumes the bot has permissions
            # to bypass NLP checks or NLP checks are disabled
            
            if getsizeof(message) < MAX_MESSAGE_SIZE:
                # strictly speaking, this bm frame is invalid,
                # but "love" is a way to identify a bot using cherry blossom ;)
                await self.send_frame("bm", "love", packed_flags, message)
