import asyncio
import os
import signal
import json

import websockets

from room import Room
from user import User

PORT = "PORT"
DEFAULT_PORT = "8001"

ROOMS = {}


async def update_number_of_online_users(room):
    all_users = room.get_emitters().union(room.get_receivers())

    event = {
        "action": "update",
        "online": len(all_users),
        "usernames": [
            {"name": user.get_username()}
            for user in room.get_emitters().union(room.get_receivers())
        ],
    }
    websockets.broadcast(
        [user.get_websocket() for user in all_users], json.dumps(event)
    )


async def maybe_delete_room(room):
    if len(room.get_emitters()) == 0:
        receivers = [user.get_websocket() for user in room.get_receivers()]
        for receiver in receivers:
            await receiver.close()

        del ROOMS[room.receiver_key]


async def play_sound(user, room):
    async for message in user.get_websocket():
        message_dict = json.loads(message)
        if message_dict["action"] == "clap":
            websockets.broadcast(
                [user.get_websocket() for user in room.get_emitters()], message
            )
            websockets.broadcast(
                [user.get_websocket() for user in room.get_receivers()], message
            )
        elif message_dict["action"] == "update_name":
            user.username = message_dict["username"]
            await update_number_of_online_users(room)


async def join_receivers(websocket, receiver_key, username):
    try:
        room = ROOMS[receiver_key]
    except KeyError:
        await websocket.close()
        return

    user = User(websocket=websocket, username=username)

    room.add_receiver(receiver_key=receiver_key, user=user)
    await update_number_of_online_users(room=room)
    try:
        await websocket.wait_closed()
    finally:
        await user.get_websocket().close()
        room.remove_receiver(user=user)
        await update_number_of_online_users(room=room)


async def join_emitters(websocket, emitter_key, receiver_key, username):
    try:
        room = ROOMS[receiver_key]
    except KeyError:
        await websocket.close()
        return

    user = User(websocket=websocket, username=username)

    room.add_emitter(emitter_key=emitter_key, user=user)
    await update_number_of_online_users(room=room)
    try:
        await play_sound(
            user=user,
            room=room,
        )
    finally:
        await user.get_websocket().close()
        room.remove_emitter(user=user)
        await update_number_of_online_users(room=room)
        await maybe_delete_room(room=room)


async def start_clapping_room(websocket, username):
    room = Room()
    user = User(websocket=websocket, username=username)
    room.add_emitter(emitter_key=room.emitter_key, user=user)
    ROOMS[room.receiver_key] = room

    try:
        event = {
            "type": "init",
            "emitter": room.emitter_key,
            "receiver": room.receiver_key,
        }
        await websocket.send(json.dumps(event))
        await play_sound(
            user=user,
            room=room,
        )
    finally:
        await user.get_websocket().close()
        room.remove_emitter(user=user)
        await update_number_of_online_users(room=room)
        await maybe_delete_room(room=room)


async def handler(websocket):
    message = await websocket.recv()
    event = json.loads(message)
    assert event["type"] == "init"

    if "emitter" in event:
        await join_emitters(
            websocket=websocket,
            emitter_key=event["emitter"],
            receiver_key=event["receiver"],
            username=event["username"],
        )
    if "receiver" in event:
        await join_receivers(
            websocket=websocket,
            receiver_key=event["receiver"],
            username=event["username"],
        )
    else:
        await start_clapping_room(websocket=websocket, username=event["username"])


async def main():
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(sig=signal.SIGTERM, callback=stop.set_result)

    port = int(os.environ.get(key=PORT, default=DEFAULT_PORT))
    async with websockets.serve(handler, "", port):
        await stop


if __name__ == "__main__":
    asyncio.run(main())
