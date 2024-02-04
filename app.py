import asyncio
import json
import os
import signal

import websockets

from server.events import get_init_room_event
from server.events import INIT
from server.logic.emitter import join_emitters
from server.logic.receiver import close_receivers_websockets
from server.logic.receiver import join_receivers
from server.model.room import Room

PORT = "PORT"
DEFAULT_PORT = "8001"

ROOMS = {}


async def handler(websocket):
    message = await websocket.recv()
    event = json.loads(message)
    assert event["type"] == INIT

    receiver_key = event.get("receiver")
    if receiver_key:
        room = ROOMS[receiver_key]
    else:
        room = await create_room(websocket)
        event["emitter"] = room.get_emitter_key()

    await join_existing_room(websocket=websocket, event=event, room=room)


async def create_room(websocket):
    room = Room()
    ROOMS[room.receiver_key] = room

    event = get_init_room_event(room=room)
    await websocket.send(json.dumps(event))
    return room


async def join_existing_room(websocket, event, room):
    if "emitter" in event:
        await join_emitters(
            websocket=websocket,
            room=room,
            emitter_key=event["emitter"],
            username=event["username"],
            user_id=event["user_id"],
            picture=event["picture"],
        )
        await maybe_delete_room(room=room)
    elif "receiver" in event:
        await join_receivers(
            websocket=websocket,
            room=room,
            receiver_key=event["receiver"],
            username=event["username"],
            user_id=event["user_id"],
            picture=event["picture"],
        )
    else:
        await websocket.close()


async def maybe_delete_room(room):
    if not room.get_emitters():
        await close_receivers_websockets(room)
        del ROOMS[room.receiver_key]


async def main():
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(sig=signal.SIGTERM, callback=stop.set_result)

    port = int(os.environ.get(key=PORT, default=DEFAULT_PORT))
    print(f"WEBSOCKET SERVER START ON PORT {port}")
    async with websockets.serve(handler, "", port):
        await stop


if __name__ == "__main__":
    asyncio.run(main())
