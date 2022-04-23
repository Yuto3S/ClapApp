import json

import websockets

from events import get_all_users_event
from events import get_single_user_update_event
from events import get_user_disconnected_event


async def get_all_users_data(room):
    all_users = room.get_all_users()

    event = get_all_users_event(all_users)
    websockets.broadcast(room.get_all_users_websocket(), json.dumps(event))


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
