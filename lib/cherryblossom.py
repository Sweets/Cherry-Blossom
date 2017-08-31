
import asyncio
import random

from .chatango.utilities import get_user_auth, room_name_is_valid
from . import profile
from .room import Room
from .privatemessages import PrivateMessages
from .messagecatcher import MessageCatcher

class Bot(object):
    def __init__(self, user_name, password):
        self.name = user_name
        self.__password = password
        self.__auth_token = get_user_auth(user_name, password)
        self.user_id = random.randint(10 ** 15, (10 ** 16) - 1)
        self.styles = profile.Style()
        self.profile = profile.Profile(self)

    def get_password(self):
        return self.__password

    def get_auth_token(self):
        return self.__auth_token

class CherryBlossom(object):
    def __init__(self, user_name, password):
        self.user = Bot(user_name, password)

        self.rooms = list()
        self.private_messages = None
        self.message_catcher = None

        self.prefix = None
        self.active = False

    def start_client(self, *rooms):
        self.rooms = rooms
        event_loop = asyncio.get_event_loop()

        try:
            event_loop.run_until_complete(
                self.initiate()
            )

            event_loop.close()
        except asyncio.CancelledError:
            pass

    async def stop(self):
        await self.private_messages.leave()
        for room in self.rooms:
            await room.leave()
        for task in asyncio.Task.all_tasks():
            task.cancel()
        self.active = False
        await self.emit_event("cherry_blossom_stop")

    def get_bot(self):
        return self.user

    async def get_room(self, room_name):
        assert room_name_is_valid(room_name), "Room name is invalid"
        room_name = room_name.lower()
        for room in self.rooms:
            if room.name == room_name:
                return room

    async def join_room(self, room_name):
        assert room_name_is_valid(room_name), "Room name is invalid"
        room_name = room_name.lower()
        if not await self.get_room(room_name):
            room = Room(room_name, self.user, self)
            asyncio.ensure_future(room.join())
            self.rooms.append(room)

    async def leave_room(self, room_name):
        assert room_name_is_valid(room_name), "Room name is invalid"
        room_name = room_name.lower()
        room = await self.get_room(room_name)
        if room:
            asyncio.ensure_future(room.leave())
            self.rooms.remove(room)

    async def emit_event(self, event_name, *args):
        if hasattr(self, event_name):
            await getattr(self, event_name)(*args)

    async def initiate(self):
        new_rooms = list()
        for room in self.rooms:
            room = Room(room, self.user, self)
            new_rooms.append(room)

        private_messages = PrivateMessages(self.user, self)

        for room in new_rooms:
            asyncio.ensure_future(room.join())
        asyncio.ensure_future(private_messages.join())

        self.rooms = new_rooms
        self.private_messages = private_messages
        self.active = True
        await self.emit_event("cherry_blossom_init")
        while self.active:
            await asyncio.sleep(1)
