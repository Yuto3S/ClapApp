import json

from server.logic.user import get_all_users_data
from server.logic.user import update_user_data
from server.model.user import User


async def join_receivers(websocket, room, receiver_key, username, user_id, picture):
    user = User(websocket=websocket, username=username, id=user_id, picture=picture)

    room.add_receiver(receiver_key=receiver_key, user=user)
    await get_all_users_data(room=room)
    try:
        await receiver_actions(user=user, room=room)
    finally:
        await user.get_websocket().close()
        room.remove_receiver(user=user)
        # TODO: Broadcast on still present users to let them know user_id has left the room
        # Instead of broadcasting to all users
        await get_all_users_data(room=room)


async def receiver_actions(user, room):
    async for message in user.get_websocket():
        message_dict = json.loads(message)
        if message_dict["action"] == "update":
            await update_user_data(room, message_dict)


async def close_receivers_websockets(room):
    for receiver in [*room.get_receivers().values()]:
        # TODO: Custom message to say that the room was closed
        await receiver.get_websocket().close()
