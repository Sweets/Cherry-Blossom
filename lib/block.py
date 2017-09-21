
class RoomBlock(object): # I should probably just remove this
    def __init__(self, room, unique_id, ip_address, user_name, _time, banned_by):
        self.room = room
        self.unique_id = unique_id
        self.ip_address = ip_address
        self.user_name = user_name
        self.time = float(_time)
        self.banned_by = banned_by

    async def remove(self):
        assert await self.room.current_user_is_moderator(), "Current user is not a moderator"
        await self.room.send_frame("removeblock",
                                   self.unique_id,
                                   self.ip_address,
                                   self.user_name)
        self.room.banned_users.remove(self)

    def __str__(self):
        return self.user_name
