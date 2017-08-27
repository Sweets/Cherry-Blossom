"""
This is the example file for the CherryBlossom module.
CherryBlossom is a library created to interface with Chatango.

The protocol used to communicate with Chatango is the WebSocket protocol
Check RFC 6455 for specification.

Every event that the library can emit is provided here, as well as
documentation on when each event is fired, as well as the arguments
for each event.

Linted with pylint 1.7.2.

To use CherryBlossom, you must have two dependencies installed,
and the Python interpreter must be running at least version 3.6.

Dependencies:
    websocket
    requests
"""

import lib

class Chatango(lib.CherryBlossom):
    """
    The `Chatango` class inherits from lib.CherryBlossom.
    Unless you are an experienced programmer,
    it's best that you stay within the realms of this
    example file.
    """

    async def cherry_blossom_init(self):
        """
        Called when the bot joins the rooms and private messages,
        just before it starts the sleep-loop.
        The "sleep-loop" is what keeps the bot from shutting
        down immediately.

        To use the in-built command handler, `prefix` must be
        defined as a string.
        """
        self.prefix = "!"

    async def cherry_blossom_stop(self):
        """
        Called when the bot is stopped, leaves all rooms and private messages,
        and stops all running async tasks. This is the last
        thing the bot does before the program stops.
        """
        pass

    #
    # Private Messages (incomplete)
    #

    async def private_messages_connected(self, client):
        """
        Called when the bot connects to private messages and receives the
        `OK` frame from the websocket.
        """
        pass

    async def private_message_received(self, client, message):
        """
        Called when the bot receives a private message.
        The `message` is a PrivateMessage object, and has 4 attributes.

        PrivateMessage.sender  | str       | Name of the sender
        PrivateMessage.time    | float     | Time it was sent
        PrivateMessage.flags   | List[str] | Flags the message has
        PrivateMessage.content | str       | Message content
        """
        pass

    #
    # Rooms
    #

    async def room_connected(self, room):
        """
        Called when the bot connects to a room and receives the
        `inited` frame from the websocket.
        """
        pass

    async def room_flags_added(self, room, flags):
        """
        Called when an administrator updates the group settings.
        In this context, `flags` are settings that were enabled.
        """
        pass

    async def room_flags_removed(self, room, flags):
        """
        Called when an administrator updates the group settings.
        In this context, `flags` are settings that were disabled.
        """
        pass

    async def room_moderator_added(self, room, moderator):
        """
        Called when an administrator adds a moderator.
        In this context, `flags` are the settings enabled for the moderator.
        """
        pass

    async def room_moderator_removed(self, room, moderator):
        """
        Called when an administrator removes/deletes a moderator.
        """
        pass

    async def room_moderator_flags_added(self, room, moderator, flags):
        """
        Called when an administrator updates a moderators settings.
        In this context, `flags` are the settings that were enabled.
        """
        pass

    async def room_moderator_flags_removed(self, room, moderator, flags):
        """
        Called when an administrator updates a moderators settings.
        In this context, `flags` are the settings that were disabled.
        """
        pass

    async def room_message_received(self, room, message):
        """
        Called when a message is sent to a room.
        The `message` is a RoomMessage object, and has 15 attributes.

        RoomMessage.sender     | str        | Name of the sender
        RoomMessage.time       | float      | Time it was sent
        RoomMessage.user_id    | int        | User id of the user
        RoomMessage.unique_id  | str        | Unique id of the user
        RoomMessage.post_id    | str        | Post id of the message
        RoomMessage.ip_address | str        | Ip address of the sender*
        RoomMessage.flags      | List[str]  | Flags the message has
        RoomMessage.deleted    | bool       | If the message was deleted or not
        RoomMessage.mentions   | List[User] | Users mentioned
        RoomMessage.font_face  | str        | Font face**
        RoomMessage.font_color | str        | Font color**
        RoomMessage.name_color | str        | Name color**
        RoomMessage.font_size  | int        | Font size**
        RoomMessage.room       | Room       | Room
        RoomMessage.content    | str        | Message content

        * Only visible if the bot is a moderator.
        ** Subject to change

        The RoomMessage object also has one member method.

        async RoomMessage.get_sender()

        Returns the User object of the sender, or None if the user is not
        logged in. User objects are created when a user joins the room,
        and when the bot connects to the room initially. They are deleted
        when a user leaves the room.
        """
        pass

    async def room_command_received(self, room, message, command, arguments):
        """
        Called when two conditions are met. One, the CherryBlossom object
        MUST have a prefix instance variable (should be assigned inside of
        `cherry_blossom_init`), and the message must begin with the prefix.
        If BOTH conditions are met, the internal command handler will
        emit this event.

        The `message` is a RoomMessage object, see above for specifications.
        The `command` is a str, and is always lowercase regardless of what the
        user sent.
        The `arguments` variable is a list of strings. These are not modified
        from the original message. Arguments in a message are delimited by a
        space (" ").
        """

        if command == "test":
            print("test")

    async def unmanaged_command(self, receiver, command, frame):
        print(receiver, command, frame)

if __name__ == "__main__":
    CHATANGO = Chatango("username", "password")
    CHATANGO.start_client("room1", "room2", "etc")
