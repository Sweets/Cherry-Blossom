
import re
import html

from .chatango.utilities import get_anonymous_user_id
from .chatango.constants import FONT_FACES
from .chatango.flags import pack_flag, unpack_flag, has_flag, MESSAGE_FLAGS

class RoomMessage(object):
    def __init__(self, room, _time, user_name, temp_name, user_id, unique_id, post_id, ip_address, flags, delimiter, *message):
        if user_name != str():
            self.sender = user_name
        else:
            if temp_name != str():
                self.sender = ";" + temp_name.lower()
            else:
                ts_id = re.search("<n(.*?)/>", message[0])
                if not isinstance(ts_id, type(None)):
                    self.sender = ":anon" + get_anonymous_user_id(ts_id.group(1), user_id)
                else:
                    self.sender = ":anon" + get_anonymous_user_id("", user_id)

        message_content = ":".join(message)
        message_style = re.search("(<n([a-zA-Z0-9]{1,6})\/>)?(<f x([\d]{0,2})([a-fA-F0-9]{6}|[a-fA-F0-9]{3}|[a-fA-F0-9]{1})=\"([a-zA-Z0-9]*)\">)?", message_content)
        if isinstance(message_style.group(1), str):
            name_color = message_style.group(2)
        else:
            name_color = "000"
        if isinstance(message_style.group(3), str):
            if message_style.group(6) != str():
                font_face = FONT_FACES.get(
                    message_style.group(6),
                    message_style.group(6)) # Get the font if it is in FONT_FACES, or the name if not.
            else:
                font_face = FONT_FACES["0"]
            if message_style.group(5) != str():
                font_color = message_style.group(5)
            else:
                font_color = "000"
            if message_style.group(4) != str():
                font_size = int(message_style.group(4))
            else:
                font_size = 12
        else:
            font_face = FONT_FACES["0"]
            font_color = "000"
            font_size = 12

        self.mentions = list()

        self.time = float(_time)
        self.user_id = int(user_id)
        self.unique_id = unique_id
        self.post_id = post_id
        self.ip_address = ip_address
        self.flags = dict()
        self.deleted = False

        for key, value in MESSAGE_FLAGS.items():
            if has_flag(flags, value):
                self.flags[key] = True
            else:
                self.flags[key] = False

        self.font_face = font_face
        self.font_color = font_color
        self.name_color = name_color
        self.font_size = font_size
        self.room = room

        self.content = html.unescape(
            re.sub("<(.*?)>", "", message_content.replace("<br/>", "\n"))
            )

        for match in re.findall("(\s)?@([a-zA-Z0-9]{1,20})(\s)?", self.content):
            for participant in self.room.participants:
                if participant.name.lower() == match[1].lower():
                    if participant not in self.mentions:
                        self.mentions.append(participant)

    async def delete(self):
        assert await self.room.current_user_is_moderator(), "Current user is not a moderator"
        await self.room.send_frame("delmsg", self.post_id)
        self.deleted = True

    async def get_sender(self):
        if self.sender[0] in [";", ":"]:
            participant = await self.room.get_participant(self.sender[1:], logged_in=False)
        else:
            participant = await self.room.get_participant(self.sender)
        return participant

    def __str__(self):
        return self.content

class PrivateMessage(object):
    def __init__(self, user_name, temp_name, unknown, _time, _flags, *message):
        self.sender = user_name.lower() # anons aren't normally allowed to PM anymore

        self.time = float(_time)
        self.flags = list()

        for key, value in MESSAGE_FLAGS.items():
            if has_flag(int(_flags), value):
                self.flags.append(key)

        self.content = html.unescape(re.sub("<(.*?)>", "", ":".join(message)))

    def __str__(self):
        return self.content
