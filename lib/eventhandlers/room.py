
import re
import time
import asyncio

from ..chatango import flags
from ..chatango.constants import GROUP_VERSION
from ..chatango.utilities import get_anonymous_user_id
from ..message import RoomMessage as Message
from ..block import RoomBlock as Block
from ..user import RoomUser as User
from ..user import RoomModerator as Moderator

async def v(room, chatango, library):
    chatango = int(chatango)
    library = int(library)
    
    if chatango > GROUP_VERSION:
        print("Chatango group version higher than library supported")
    elif GROUP_VERSION > library:
        print("Chatango group version lower than library supported")

async def ok(room, owner, user_id, state, user_name, _time, ip_address, mods, _flags):
    room.owner = owner

    unpacked_flags = list()
    for key, value in flags.ROOM_FLAGS.items():
        if flags.has_flag(_flags, value):
            unpacked_flags.append(key)

    room.flags = unpacked_flags

    if mods != str():
        for mod in mods.split(";"):
            name, _flags = mod.split(",")
            moderator = Moderator(room, name, _flags)
            room.moderators.append(moderator)

async def inited(room):
    await room.send_frame("g_participants", "start")
    # prefer g_participants over gparticipants
    # Former is legacy, latter is HTML5/current,
    # legacy is more verbose
    await room.send_frame("getbannedwords")
    await room.send_frame("getratelimit")
    if await room.current_user_is_moderator():
        await room.send_frame("blocklist", "block", "", "next", 500)
    await room.emit_event("room_connected")

async def g_participants(room, *args):
    for participant in ":".join(args).split(";"):
        room.participants.append(
            User(room, *participant.split(":"))
        )
    room.user_count = len(room.participants)

async def blocklist(room, *args):
    if len(args) and args[0] != str():
        blocklist = ":".join(args).split(";")
        for ban in blocklist:
            ban = ban.split(":")
            record = Block(room, *ban)
            room.banned_users.append(record)
        await room.send_frame("blocklist", "block", ban[3], "next", 500)

async def bw(room, partial, exact):
    room.banned_words["partial"] = partial.split("%2C")
    room.banned_words["exact"] = exact.split("%2C")

async def getratelimit(room, interval, something):
    pass

async def groupflagsupdate(room, _flags):
    old_flags = room.flags

    unpacked_flags = list()
    for key, value in flags.ROOM_FLAGS.items():
        if flags.has_flag(_flags, value):
            unpacked_flags.append(key)

    removed_flags = list()
    added_flags = list()

    for flag in unpacked_flags:
        if flag not in old_flags:
            added_flags.append(flag)

    for flag in old_flags:
        if flag not in unpacked_flags:
            removed_flags.append(flag)

    if len(removed_flags) >= 1:
        await room.emit_event("room_flags_removed", removed_flags)

    if len(added_flags) >= 1:
        await room.emit_event("room_flags_added", added_flags)

    room.flags = unpacked_flags

async def mods(room, *moderators):
    old_moderators = room.moderators
    new_moderators = list()

    if len(moderators) == 1:
        if moderators[0] == "":
            moderators = list()

    for moderator_string in moderators:
        moderator_name, moderator_flags = moderator_string.split(",")
        moderator = Moderator(room, moderator_name, moderator_flags);
        new_moderators.append(moderator);

    room.moderators = new_moderators

    checked_moderators = list()

    for moderator in old_moderators:
        if moderator in new_moderators:
            added_flags = list()
            removed_flags = list()

            old_flags = moderator.packed_flags
            old_flags_array = list()
            new_flags = (await room.get_moderator(moderator.name)).packed_flags
            new_flags_array = list()

            for key, value in flags.MODERATOR_FLAGS.items():
                if flags.has_flag(old_flags, value):
                    old_flags_array.append(key)
                if flags.has_flag(new_flags, value):
                    new_flags_array.append(key)

            for flag in old_flags_array:
                if flag not in new_flags_array:
                    removed_flags.append(flag)

            for flag in new_flags_array:
                if flag not in old_flags_array:
                    added_flags.append(flag)

            if len(added_flags) >= 1:
                await room.emit_event("room_moderator_flags_added", moderator, added_flags)

            if len(removed_flags) >= 1:
                await room.emit_event("room_moderator_flags_removed", moderator, removed_flags)

            checked_moderators.append(moderator.name)

        else:
            await room.emit_event("room_moderator_removed", moderator)

    for moderator in new_moderators:
        if moderator.name not in checked_moderators:
            await room.emit_event("room_moderator_added", moderator)

async def n(room, user_count):
    room.user_count = int(user_count, 16)

async def premium(room, _flags, _time):
    if int(_time) > time.time():
        await room.send_frame("msgbg", 1)

async def i(room, *args):
    await b(room, *args)

async def b(room, *args):
    message = Message(room, *args)
    room.messages.setdefault(message.post_id, message)

async def u(room, old_id, new_id):
    message = room.messages.get(old_id, None)

    while isinstance(message, type(None)):
        await asyncio.sleep(0.1)
        message = room.messages.get(old_id, None)

    message.post_id = new_id

    sender = await message.get_sender()
    if sender:
        sender.messages.append(message)

    if message.content:
        if room.user.name[0] in [":", ";"]:
            user_name = room.user.name[1:]
        else:
            user_name = room.user.name
        ping = re.search("@" + user_name, message.content, re.IGNORECASE)
        if room.controller.prefix and type(room.controller.prefix) is str:
            if message.content.startswith(room.controller.prefix):
                command = message.content.lstrip(room.controller.prefix).split(" ")
                arguments = command[1:]
                command = command[0].lower()
                await room.emit_event("room_command_received", message, command, arguments)
            else:
                if not isinstance(ping, type(None)):
                    await room.emit_event("room_mentioned", message)
                else:
                    await room.emit_event("room_message_received", message)
        else:
            if not isinstance(ping, type(None)):
                await room.emit_event("room_mentioned", message)
            else:
                await room.emit_event("room_message_received", message)

async def msglexceeded(room, limit):
    await room.emit_event("room_message_length_exceeded")

async def show_fw(room):
    pass # Show flood warning

async def show_tb(room, _time):
    pass # Show time ban

async def tb(room, _time):
    pass

async def climited(room, *frame):
    pass # Climited

async def show_nlp(room, _flags):
    pass # Auto moderation

async def ubw(room):
    await room.send_frame("getbannedwords")
    await room.emit_event("room_banned_words_updated")

async def participant(room, action, session_id, user_id, user_name, temp_name, ip_address, _time):
    action = int(action)

    if action == 0:
        # user left
        participant = await room.get_participant(user_name)
        if participant:
            room.participants.remove(participant)

            for _participant in room.participants:
                if participant == _participant:
                    return # They've got another session with the same user
            # No other sessions
            await room.emit_event("room_user_left", participant)

    elif action == 1:
        # user joined
        participant = User(room,
                           session_id,
                           _time,
                           user_id,
                           user_name,
                           temp_name,
                           ip_address)

        should_emit_event = True
        for _participant in room.participants:
            if participant == _participant:
                should_emit_event = False

        room.participants.append(participant)
        if should_emit_event:
            await room.emit_event("room_user_joined", participant)

    elif action == 2:
        # name change performed, identify users by session id
        for participant in room.participants:
            if participant.session_id == session_id:
                # Found participant
                users_new_name = str()

                if user_name == "None":
                    if temp_name == "None":
                        users_new_name = "anon" + get_anonymous_user_id(
                            _time.split(".")[0][-4:], user_id)
                    else:
                        users_new_name = temp_name.lower()
                    logged_in = False
                else:
                    users_new_name = user_name.lower()
                    logged_in = True

                users_old_name = participant.name

                participant.name = users_new_name
                participant.logged_in = logged_in

                await room.emit_event("room_user_changed_name",
                                      participant,
                                      users_old_name,
                                      users_new_name)

async def clearall(room, _ok):
    if _ok == 'ok': # ???
        for message in room.messages.values():
            message.deleted = True
        await room.emit_event("room_cleared")

async def deleteall(room, *post_ids):
    last_post = None
    for post_id in post_ids:
        message = room.messages.get(post_id, None)
        if message:
            message.deleted = True
            last_post = message
    if last_post:
        await room.emit_event("room_user_messages_deleted", last_post.sender)

async def delete(room, post_id):
    message = room.messages.get(post_id, None)
    if message:
        message.deleted = True
        await room.emit_event("room_user_message_deleted", message)
