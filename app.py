import asyncio
import os
import secrets
import signal
import json

import websockets

PORT = "PORT"
DEFAULT_PORT = "8001"

ACTIVE_CLAPPERS = {}  # Can receive and send Clapp messages to everyone
PASSIVE_CLAPPERS = {}  # Can only receive Clapp messages


async def play_sound(websocket, active_key):
    async for message in websocket:
        message = json.loads(message)
        print(message)
        event = {"action": "clap"}
        print(f"websocket {id(websocket)}, length: {len(ACTIVE_CLAPPERS[active_key])}")
        websockets.broadcast(ACTIVE_CLAPPERS[active_key], json.dumps(event))


async def join_active(websocket, active_key):
    active_clappers = ACTIVE_CLAPPERS[active_key]
    active_clappers.add(websocket)
    try:
        await play_sound(websocket, active_key)
    finally:
        active_clappers.remove(websocket)
        if len(ACTIVE_CLAPPERS[active_key]) == 0:
            del ACTIVE_CLAPPERS[active_key]


async def start(websocket):
    active_key = secrets.token_urlsafe(12)

    ACTIVE_CLAPPERS[active_key] = {websocket}
    active_clappers = ACTIVE_CLAPPERS[active_key]

    try:
        event = {
            "type": "init",
            "active": active_key,
        }
        await websocket.send(json.dumps(event))
        await play_sound(websocket, active_key)
    finally:
        active_clappers.remove(websocket)
        if len(ACTIVE_CLAPPERS[active_key]) == 0:
            del ACTIVE_CLAPPERS[active_key]


async def handler(websocket):
    message = await websocket.recv()
    event = json.loads(message)
    print(event)
    assert event["type"] == "init"

    if "active" in event:
        await join_active(websocket, event["active"])
    else:
        await start(websocket)


async def main():
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(sig=signal.SIGTERM, callback=stop.set_result)

    port = int(os.environ.get(key=PORT, default=DEFAULT_PORT))
    async with websockets.serve(handler, "", port):
        await stop


if __name__ == "__main__":
    asyncio.run(main())
