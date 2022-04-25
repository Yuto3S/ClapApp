import json

from server.logic.user import add_user_to_room
from server.logic.user import remove_user_from_room
from server.logic.user import update_user_data


async def join_receivers(websocket, room, receiver_key, username, user_id, picture):
    user = await add_user_to_room(
        room=room,
        websocket=websocket,
        username=username,
        user_id=user_id,
        picture=picture,
        receiver_key=receiver_key,
    )

    try:
        await receiver_actions(user=user, room=room)
    finally:
        await remove_user_from_room(room=room, user=user, receiver_key=receiver_key)


async def receiver_actions(user, room):
    async for message in user.get_websocket():
        # import ipdb; ipdb.set_trace()
        message_dict = json.loads(message)
        if message_dict["action"] == "update":
            await update_user_data(room, message_dict)


async def close_receivers_websockets(room):
    for receiver in [*room.get_receivers().values()]:
        # TODO: Custom message to say that the room was closed
        await receiver.get_websocket().close()
