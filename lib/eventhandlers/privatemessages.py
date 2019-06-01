
import time

from ..message import PrivateMessage as Message
from ..user import Friend

async def seller_name(client, user_name, session_id):
    pass

async def _time(client, *args):
    pass

async def OK(client):
    await client.send_frame("wl")
    await client.send_frame("getblock")
    await client.emit_event("private_messages_connected")

async def denied(client):
    await client.emit_event("private_messages_denied")
    
async def premium(client, flags, _time):
    if int(_time) > time.time():
        await client.send_frame("msgbg", 1)

async def wl(client, *friend_list):
    if len(client.friends) >= 1:
        client.friends = list()
    
    for index in range(0, len(friend_list), 4):
        friend_data = friend_list[index:index + 4]
        friend = Friend(client, *friend_data)
        
        client.friends.append(friend)
        await client.send_frame("track", friend.name)

async def wladd(client, user_name, status, _time):
    if status == "invalid":
        return
    
    friend = await client.get_friend(user_name)
    if not friend:
        friend = Friend(client, user_name, time.time(), status, _time)
        client.friends.append(friend)
        
        await client.emit_event("private_messages_friend_added", friend)
        await client.send_frame("wl")
        await client.send_frame("track", user_name.lower())

async def wldelete(client, user_name, status, unknown):
    friend = await client.get_friend(user_name)
    if friend and status == "deleted":
        for _friend in client.friends:
            if _friend.name == friend.name:
                client.friends.remove(_friend)
                await client.emit_event("private_messages_friend_deleted", user_name)

async def wlonline(client, user_name, _time):
    pass # Users that are set to be tracked (track frame) are output in status
    # No need to take advantage of wlonline, since all users are tracked

async def wloffline(client, user_name, _time):
    pass

async def wlapp(client, user_name, _time):
    pass

async def status(client, user_name, _time, status, unknown):
    friend = await client.get_friend(user_name)
    if friend:
        friend.last_active = float(_time)
        friend.idle = False
        friend.status = status
        
        if status == "online":
            await client.emit_event("private_messages_friend_online", friend)
        else:
            await client.emit_event("private_messages_friend_offline", friend)

async def track(client, user_name, _time, status):
    friend = Friend(client, user_name, _time, status, _time)
    
    if status == "online":
        friend.last_active = time.time() - (int(_time) * 60)
    elif status == "offline":
        friend.last_active = float(_time)
    
    await client.emite_event("private_messages_friend_added", friend)

async def idleupdate(client, user_name, idle_status):
    friend = await client.get_friend(user_name)
    if friend:
        friend.idle = idle_status == "0"
        friend.last_active = time.time()
    
async def msg(client, *args):
    await client.emit_event("private_messages_message_received", Message(*args))

# Still needs a LOT of work, if it's not apparent
