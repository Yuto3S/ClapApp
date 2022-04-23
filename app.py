import asyncio
import os
import signal
import json

import websockets

from server.logic.emitter import join_emitters, start_clapping_room
from server.logic.receiver import join_receivers
from server.model.room import Room

PORT = "PORT"
DEFAULT_PORT = "8001"

ROOMS = {}


async def maybe_delete_room(room):
    if not room.get_emitters():
        receivers = [user.get_websocket() for user in room.get_receivers()]
        for receiver in receivers:
            await receiver.close()

        del ROOMS[room.receiver_key]


async def handler(websocket):
    message = await websocket.recv()
    event = json.loads(message)
    assert event["type"] == "init"

    if "emitter" in event:
        try:
            room = ROOMS[event["receiver"]]
        except KeyError:
            await websocket.close()
            return

        await join_emitters(
            websocket=websocket,
            room=room,
            emitter_key=event["emitter"],
            receiver_key=event["receiver"],
            username=event["username"],
            user_id=event["user_id"],
            picture=event["picture"],
        )
    if "receiver" in event:
        try:
            room = ROOMS[event["receiver"]]
        except KeyError:
            await websocket.close()
            return

        await join_receivers(
            websocket=websocket,
            room=room,
            receiver_key=event["receiver"],
            username=event["username"],
            user_id=event["user_id"],
            picture=event["picture"],
        )
    else:
        room = Room()
        ROOMS[room.receiver_key] = room

        await start_clapping_room(
            websocket=websocket,
            room=room,
            username=event["username"],
            user_id=event["user_id"],
            picture=event["picture"],
        )


async def main():
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(sig=signal.SIGTERM, callback=stop.set_result)

    port = int(os.environ.get(key=PORT, default=DEFAULT_PORT))
    async with websockets.serve(handler, "", port):
        await stop


if __name__ == "__main__":
    asyncio.run(main())
