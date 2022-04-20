import asyncio
import os
import secrets
import signal
import json

import websockets

PORT = "PORT"
DEFAULT_PORT = "8001"

ACTIVE_CLAPPERS = {}  # Can receive and send Clapp messages to everyone


def cleanup_room(websocket, active_clappers, active_key):
    active_clappers.remove(websocket)
    if len(ACTIVE_CLAPPERS[active_key]) == 0:
        del ACTIVE_CLAPPERS[active_key]


async def play_sound(websocket, active_key):
    async for message in websocket:
        message_dict = json.loads(message)
        assert message_dict["action"] == "clap"
        websockets.broadcast(ACTIVE_CLAPPERS[active_key], message)


async def join_active_clapping_room(websocket, active_key):
    active_clappers = ACTIVE_CLAPPERS[active_key]
    active_clappers.add(websocket)
    try:
        await play_sound(websocket=websocket, active_key=active_key)
    finally:
        cleanup_room(
            websocket=websocket, active_clappers=active_clappers, active_key=active_key
        )


async def start_clapping_room(websocket):
    active_key = secrets.token_urlsafe(12)

    active_clappers = {websocket}
    ACTIVE_CLAPPERS[active_key] = active_clappers

    try:
        event = {
            "type": "init",
            "active": active_key,
        }
        await websocket.send(json.dumps(event))
        await play_sound(websocket=websocket, active_key=active_key)
    finally:
        cleanup_room(
            websocket=websocket, active_clappers=active_clappers, active_key=active_key
        )


async def handler(websocket):
    message = await websocket.recv()
    event = json.loads(message)
    assert event["type"] == "init"

    if "active" in event:
        await join_active_clapping_room(websocket=websocket, active_key=event["active"])
    else:
        await start_clapping_room(websocket=websocket)


async def main():
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(sig=signal.SIGTERM, callback=stop.set_result)

    port = int(os.environ.get(key=PORT, default=DEFAULT_PORT))
    async with websockets.serve(handler, "", port):
        await stop


if __name__ == "__main__":
    asyncio.run(main())
