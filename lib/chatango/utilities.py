
import re
import requests

from . import constants

def get_user_auth(user_name: str, password: str) -> str:
    """
    Gets user authentication token to edit profile or login to private messages
    """
    assert user_name_is_valid(user_name), "User name is invalid"
    assert type(password) is str, "password is not a string."

    user_name = user_name.lower()

    try:
        payload_data = {
            "user_id": user_name,
            "password": password,
            "storecookie": "on",
            "checkerrors": "yes"
        }
        request = requests.post("http://chatango.com/login", data=payload_data)
        token = request.cookies.get("auth.chatango.com", None)
        if isinstance(token, type(None)):
            print("Nope")
            #raise errors.AuthenticationError("Incorrect credentials supplied.")
            # I really need not just print "Nope", and raise an error. But for the moment, I'm just dumping the library.
        else:
            return token
    except Exception:
        pass

def get_room_server(room_name: str) -> str:
    """
    Gets the weight associated with the room name and returns a server string
    room_name string
    """
    assert room_name_is_valid(room_name), "Room name is invalid"
    room_name = room_name.lower()

    if room_name in constants.FIXED_WEIGHTS:
        return "s" + str(
            constants.FIXED_WEIGHTS[room_name]
            ) + ".chatango.com"

    room_name = re.sub("-|_", "q", room_name)
    length = min(5, len(room_name))
    gnum = int(room_name[0:length], 36)
    mod_str = room_name[6:6 + min(3, len(room_name) - 5)] or "0"
    mod = max(int(mod_str, 36), 1000)
    position = (gnum % mod) / mod
    total_weights = sum(server for weight, server in constants.SERVER_MAP)
    base_num = 0
    weight = None

    for weight, server in constants.SERVER_MAP:
        base_num += (server / total_weights)
        if position <= base_num:
            return "s" + str(weight) + ".chatango.com"
    return ""

def get_anonymous_user_id(ts_id: str, anon_id: str) -> str:
    assert type(ts_id) is str, "ts_id is not a string"
    assert type(anon_id) is str, "anon_id is not a string"

    if len(ts_id) != 4:
        ts_id = "3452"
    if len(anon_id) > 8:
        anon_id = anon_id[:8]

    number = anon_id[-4:]
    output = list()

    for index in range(0, len(number)):
        alpha = int(number[index:index + 1])
        beta = int(ts_id[index:index + 1])

        output.append(
            str(alpha + beta)[-1:]
            )
    return "".join(output)

def user_name_is_valid(user_name: str, allow_unregistered: bool = False) -> bool:
    assert type(user_name) is str, "User name is not a string"
    user_name = user_name.lower()

    if allow_unregistered:
        expr = re.compile("^([a-z0-9]{1,20}|[;:][a-z0-9]{1,20})$")
    else:
        expr = re.compile("^([a-z0-9]{1,20})$")

    if expr.match(user_name):
        return True

    return False

def room_name_is_valid(room_name: str) -> bool:
    assert type(room_name) is str, "Room name is not a string"
    room_name = room_name.lower()

    expr = re.compile("^([a-z0-9\-_]{1,20})$")

    if expr.match(room_name):
        return True

    return False
