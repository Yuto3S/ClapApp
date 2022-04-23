""" TODO:
1) Single socket send the list of all the users to the new user
2) Broadcast creation of new user to existing ones
"""
import json

import websockets

from events import get_all_users_event, get_single_user_update_event


async def get_all_users_data(room, user):
    all_users = room.get_all_users()

    event = get_all_users_event(all_users)
    websockets.broadcast(
        [user.get_websocket() for user in room.get_all_users().values()],
        json.dumps(event),
    )
    # await user.get_websocket().send(json.dumps(event))


async def update_user_data(room, data):
    user = room.get_user(data.get("user_id"))
    match data.get("update"):
        case "username":
            user.update_name(data.get("username"))
        case "picture":
            user.update_picture(data.get("picture"))

    event = get_single_user_update_event(user)

    websockets.broadcast(
        [user.get_websocket() for user in room.get_all_users().values()],
        json.dumps(event),
    )
