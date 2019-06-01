
from .chatango.utilities import get_anonymous_user_id
from .block import RoomBlock as Block
from .chatango import flags

class RoomModerator(object):
    def __init__(self, room, user_name, _flags):
        self.room = room
        self.name = user_name.lower()

        self.packed_flags = _flags
        self.flags = dict()

        for key, value in flags.MODERATOR_FLAGS.items():
            if flags.has_flag(_flags, value):
                self.flags[key] = True
            else:
                self.flags[key] = False

    async def disable_flags(self, *_flags):
        assert await self.room.current_user_is_moderator(), "Current user is not a moderator"
        current_user = await self.room.get_current_user()

        if not await current_user.is_owner():
            moderator = self.room.get_moderator(current_user.name.lower())
            if moderator:
                if not moderator.has_flag("edit_mods"):
                    return
            else:
                return

        if self.name != current_user.name.lower():
            packed_flags = 0

            for flag in self.flags.keys():
                flag_name = flag
                if flag_name in flags.MODERATOR_FLAGS.keys():
                    if flag not in _flags:
                        flag_value = flags.MODERATOR_FLAGS.get(flag_name)
                        packed_flags = flags.pack_flag(packed_flags, flag_value)
                    else:
                        self.flags[flag_name] = False
            await self.room.send_frame("updmod", self.name, packed_flags)
            self.packed_flags = packed_flags


    async def enable_flags(self, *_flags):
        assert await self.room.current_user_is_moderator(), "Current user is not a moderator"
        current_user = await self.room.get_current_user()

        if not await current_user.is_owner():
            moderator = self.room.get_moderator(current_user.name.lower())
            if moderator:
                if not moderator.has_flag("edit_mods"):
                    return
            else:
                return

        if self.name != current_user.name.lower():
            packed_flags = 0
            add_admin_flags = False

            for flag in _flags:
                flag_name = flag
                if flag_name in flags.MODERATOR_FLAGS.keys():
                    flag_value = flags.MODERATOR_FLAGS.get(flag_name)
                    if flag_name in flags.ADMINISTRATOR_ONLY:
                        add_admin_flags = True
                    packed_flags = flags.pack_flag(packed_flags, flag_value)
                    self.flags[flag_name] = True

            if add_admin_flags:
                for flag in flags.ADMINISTRATOR_REQUIRED:
                    flag_name = flag
                    flag_value = flags.MODERATOR_FLAGS.get(flag)
                    packed_flags = flags.pack_flag(packed_flags, flag_value)
                    self.flags[flag_name] = True
            await self.room.send_frame("updmod", self.name, packed_flags)
            self.packed_flags = packed_flags

    async def has_flag(self, _flag):
        return self.flags.get(_flag, False)

    def __str__(self):
        return self.name

    def __eq__(self, alternative):
        return self.name == alternative.name

class RoomUser(object):
    def __init__(self, room, session_id, join_time, user_id, user_name, temp_name, ip_address):
        self.room = room
        if user_name == "None":
            if temp_name == "None":
                self.name = ":anon" + get_anonymous_user_id(
                        join_time.split(".")[0][-4:], user_id)
            else:
                self.name = ";" + temp_name.lower()
            self.logged_in = False
        else:
            self.name = user_name
            self.logged_in = True
        self.session_id = session_id
        self.join_time = float(join_time)
        self.user_id = user_id
        self.ip_address = ip_address
        self.messages = list()

    async def is_anonymous(self):
        return not self.logged_in

    async def is_temporary(self):
        return not self.logged_in and self.name != str()

    async def is_banned(self):
        ban_record = await self.room.get_block(self.name.lower())
        if ban_record:
            return True
        return False

    async def is_moderator(self):
        if not await self.is_anonymous() and not await self.is_temporary():
            return (await self.room.get_moderator(self.name.lower())) != None
        return False

    async def is_administrator(self):
        if not await self.is_anonymous() and not await self.is_temporary():
            if await self.is_moderator():
                moderator = await self.room.get_moderator()
                return await moderator.has_flag("edit_group")
            else:
                return self.room.owner == self.name.lower()
        return False

    async def is_owner(self):
        if not await self.is_anonymous() and not await self.is_temporary():
            return self.room.owner == self.name.lower()
        return False

    async def get_last_message(self):
        for message in sorted(self.messages, key=lambda x: x.time, reverse=True):
            if not message.deleted:
                return message

    async def delete_messages(self):
        assert await self.room.current_user_is_moderator(), "Current user is not a moderator"
        last_message = await self.get_last_message()
        if last_message:
            await self.room.send_frame("delallmsg",
                                       last_message.unique_id,
                                       last_message.ip_address,
                                       self.name.lower())
            for message in self.messages:
                if not message.deleted:
                    message.deleted = True

    async def block(self):
        assert await self.room.current_user_is_moderator(), "Current user is not a moderator"
        last_message = await self.get_last_message()
        if last_message:
            if self.name[0] in [":", ";"]:
                name = ""
            else:
                name = self.name.lower()
            await self.room.send_frame("block",
                                       last_message.unique_id,
                                       last_message.ip_address,
                                       name)
            record = Block(self.room,
                           last_message.unique_id,
                           last_message.ip_address,
                           name,
                           time.time(),
                           (await self.room.get_current_user()).name.lower())
            self.room.banned_users.append(record)

    async def unblock(self):
        if self.is_banned():
            record = await self.room.get_block(self.name.lower())
            if record:
                record.remove()

    def __str__(self):
        return name

    def __eq__(self, alternative):
        return self.name == alternative.name

class Friend(object):
    def __init__(self, client, user_name, _time, status, idle_time):
        self.client = client
        self.name = user_name # names are already lowered in PMs
        self.status = status
        self.__sender_profile = None # TODO
        
        if status == "on" and int(idle_time) >= 1:
            self.idle = True
            self.last_active = time.time() - (int(idle_time) * 60)
        else:
            self.idle = False
            self.last_active = float(_time)

    async def is_online(self):
        return self.status == "online"

    async def is_offline(self):
        return self.status in ["offline", "app"]
    
    async def is_on_mobile(self):
        return self.status == "app"
   
    async def send_message(self, *message):
        await self.client.send_message(*message, recipient=self.name)

    def __str__(self):
        return self.name
    
