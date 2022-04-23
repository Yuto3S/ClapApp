import json

import websockets

from server.logic.user import add_user_to_room
from server.logic.user import remove_user_from_room
from server.logic.user import update_user_data


async def join_emitters(websocket, room, emitter_key, username, user_id, picture):
    user = await add_user_to_room(
        room=room,
        websocket=websocket,
        username=username,
        user_id=user_id,
        picture=picture,
        emitter_key=emitter_key,
    )
    try:
        await emitter_actions(user=user, room=room)
    finally:
        await remove_user_from_room(room=room, user=user, emitter_key=emitter_key)


async def emitter_actions(user, room):
    async for message in user.get_websocket():
        message_dict = json.loads(message)
        if message_dict["action"] == "clap":
            websockets.broadcast(room.get_all_users_websocket(), message)
        elif message_dict["action"] == "update":
            await update_user_data(room, message_dict)
