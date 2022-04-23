import json

import websockets

from app import maybe_delete_room
from server.logic.user import get_all_users_data, update_user_data
from server.model.user import User


async def start_clapping_room(websocket, room, username, user_id, picture):
    user = User(websocket=websocket, username=username, id=user_id, picture=picture)
    room.add_emitter(emitter_key=room.emitter_key, user=user)

    await get_all_users_data(room=room, user=user)
    try:
        event = {
            "type": "init",
            "emitter": room.emitter_key,
            "receiver": room.receiver_key,
        }
        await websocket.send(json.dumps(event))
        await emitter_actions(
            user=user,
            room=room,
        )
    finally:
        await delete_emitter(room, user)
        """TODO specific call when a single user is removed to the other broadcasters"""
        await get_all_users_data(room=room, user=user)


async def join_emitters(
    websocket, room, emitter_key, receiver_key, username, user_id, picture
):
    user = User(websocket=websocket, username=username, id=user_id, picture=picture)

    room.add_emitter(emitter_key=emitter_key, user=user)
    await get_all_users_data(room=room, user=user)
    try:
        await emitter_actions(
            user=user,
            room=room,
        )
    finally:
        await delete_emitter(room, user)
        """TODO specific call when a single user is removed to the other broadcasters"""
        await get_all_users_data(room=room, user=user)


async def delete_emitter(room, user):
    await user.get_websocket().close()
    room.remove_emitter(user=user)
    await maybe_delete_room(room=room)


async def emitter_actions(user, room):
    async for message in user.get_websocket():
        message_dict = json.loads(message)
        if message_dict["action"] == "clap":
            all_users = room.get_all_users()
            users = [all_users[user_id].get_websocket() for user_id in all_users]
            websockets.broadcast(users, message)
        elif message_dict["action"] == "update":
            await update_user_data(room, message_dict)
