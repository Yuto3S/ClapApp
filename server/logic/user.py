import json

import websockets

from events import get_all_users_event
from events import get_notify_existing_users_of_new_user_event
from events import get_single_user_update_event
from events import get_user_disconnected_event
from server.model.user import User


async def add_user_to_room(
    room, websocket, username, user_id, picture, emitter_key=None, receiver_key=None
):
    user = User(websocket=websocket, username=username, id=user_id, picture=picture)
    room.add_user(user=user, emitter_key=emitter_key, receiver_key=receiver_key)
    await get_all_users_data(room=room, websocket=websocket)
    await notify_existing_users(room=room, new_user_websocket=websocket, new_user=user)
    return user


async def remove_user_from_room(room, user, emitter_key=None, receiver_key=None):
    await user.get_websocket().close()
    room.remove_user(user=user, emitter_key=emitter_key, receiver_key=receiver_key)
    await user_disconnected(room=room, user=user)


async def get_all_users_data(room, websocket):
    all_users = room.get_all_users()

    event = get_all_users_event(all_users)
    await websocket.send(json.dumps(event))


async def notify_existing_users(room, new_user_websocket, new_user):
    existing_users_websocket = [
        websocket
        for websocket in room.get_all_users_websocket()
        if websocket != new_user_websocket
    ]
    event = get_notify_existing_users_of_new_user_event(new_user)
    websockets.broadcast(existing_users_websocket, json.dumps(event))


async def update_user_data(room, data):
    user = room.get_user(data.get("user_id"))
    match data.get("update"):
        case "username":
            user.update_name(data.get("username"))
        case "picture":
            user.update_picture(data.get("picture"))

    event = get_single_user_update_event(user)
    websockets.broadcast(room.get_all_users_websocket(), json.dumps(event))


async def user_disconnected(room, user):
    event = get_user_disconnected_event(user)
    websockets.broadcast(room.get_all_users_websocket(), json.dumps(event))
