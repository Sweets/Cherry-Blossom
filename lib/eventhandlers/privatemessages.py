
import time

from ..message import PrivateMessage as Message

async def _time(client, *args):
    print(*args)

async def OK(client):
    await client.send_frame("getblock")
    await client.emit_event("private_messages_connected")

async def premium(client, flags, _time):
    if int(_time) > time.time():
        await client.send_frame("msgbg", 1)

async def msg(client, *args):
    await client.emit_event("private_messages_message_received", Message(*args))

# Still needs a LOT of work, if it's not apparent
