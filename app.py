import asyncio
import os
import secrets
import signal
import json

import websockets

PORT = "PORT"
DEFAULT_PORT = "8001"

EMITTERS = {}  # Can receive and send Clapp messages to everyone
RECEIVERS = {}


def cleanup_room(websocket, active_emitters, emitter_key):
    active_emitters.remove(websocket)
    if len(EMITTERS[emitter_key]) == 0:
        del EMITTERS[emitter_key]


async def play_sound(websocket, emitter_key):
    async for message in websocket:
        message_dict = json.loads(message)
        assert message_dict["action"] == "clap"
        websockets.broadcast(EMITTERS[emitter_key], message)


async def join_active_clapping_room(websocket, emitter_key):
    active_emitters = EMITTERS[emitter_key]
    active_emitters.add(websocket)
    try:
        await play_sound(websocket=websocket, emitter_key=emitter_key)
    finally:
        cleanup_room(
            websocket=websocket,
            active_emitters=active_emitters,
            emitter_key=emitter_key,
        )


async def start_clapping_room(websocket):
    emitter_key = secrets.token_urlsafe(12)

    active_emitters = {websocket}
    EMITTERS[emitter_key] = active_emitters

    try:
        event = {
            "type": "init",
            "emitter": emitter_key,
        }
        await websocket.send(json.dumps(event))
        await play_sound(websocket=websocket, emitter_key=emitter_key)
    finally:
        cleanup_room(
            websocket=websocket,
            active_emitters=active_emitters,
            emitter_key=emitter_key,
        )


async def handler(websocket):
    message = await websocket.recv()
    event = json.loads(message)
    assert event["type"] == "init"

    if "emitter" in event:
        await join_active_clapping_room(
            websocket=websocket, emitter_key=event["emitter"]
        )
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
