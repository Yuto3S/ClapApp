import json

import websockets

from server.logic.user import get_all_users_data
from server.logic.user import update_user_data
from server.model.user import User


async def join_emitters(websocket, room, emitter_key, username, user_id, picture):
    user = User(websocket=websocket, username=username, id=user_id, picture=picture)
    room.add_emitter(emitter_key=emitter_key, user=user)

    await get_all_users_data(room=room)
    try:
        await emitter_actions(
            user=user,
            room=room,
        )
    finally:
        await delete_emitter(room, user)
        # TODO: Broadcast on still present users to let them know user_id has left the room
        # Instead of broadcasting to all users
        await get_all_users_data(room=room)


async def delete_emitter(room, user):
    await user.get_websocket().close()
    room.remove_emitter(user=user)


async def emitter_actions(user, room):
    async for message in user.get_websocket():
        message_dict = json.loads(message)
        if message_dict["action"] == "clap":
            all_users = room.get_all_users()
            users = [all_users[user_id].get_websocket() for user_id in all_users]
            websockets.broadcast(users, message)
        elif message_dict["action"] == "update":
            await update_user_data(room, message_dict)
