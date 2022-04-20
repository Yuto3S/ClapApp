import asyncio
import os
import secrets
import signal
import json

import websockets

PORT = "PORT"
DEFAULT_PORT = "8001"

EMITTERS = {}  # Can receive and send Clap messages to everyone
RECEIVERS = {}  # Can only receive Clap messages


def cleanup_room(websocket, emitters, emitter_key, receiver_key):
    emitters.remove(websocket)
    if len(EMITTERS[emitter_key]) == 0:
        del EMITTERS[emitter_key]
        del RECEIVERS[receiver_key]


async def play_sound(websocket, emitter_key, receiver_key):
    async for message in websocket:
        message_dict = json.loads(message)
        assert message_dict["action"] == "clap"
        websockets.broadcast(EMITTERS[emitter_key], message)
        websockets.broadcast(RECEIVERS[receiver_key], message)


async def join_receivers(websocket, receiver_key):
    receivers = RECEIVERS[receiver_key]
    receivers.add(websocket)
    try:
        await websocket.wait_closed()
    finally:
        receivers.remove(websocket)


async def join_emitters(websocket, emitter_key, receiver_key):
    emitters = EMITTERS[emitter_key]
    emitters.add(websocket)
    try:
        await play_sound(
            websocket=websocket, emitter_key=emitter_key, receiver_key=receiver_key
        )
    finally:
        cleanup_room(
            websocket=websocket,
            emitters=emitters,
            emitter_key=emitter_key,
            receiver_key=receiver_key,
        )


async def start_clapping_room(websocket):
    emitter_key = secrets.token_urlsafe(12)
    receiver_key = secrets.token_urlsafe(12)

    emitters = {websocket}
    EMITTERS[emitter_key] = emitters
    RECEIVERS[receiver_key] = set()

    try:
        event = {
            "type": "init",
            "emitter": emitter_key,
            "receiver": receiver_key,
        }
        await websocket.send(json.dumps(event))
        await play_sound(
            websocket=websocket, emitter_key=emitter_key, receiver_key=receiver_key
        )
    finally:
        cleanup_room(
            websocket=websocket,
            emitters=emitters,
            emitter_key=emitter_key,
            receiver_key=receiver_key,
        )


async def handler(websocket):
    message = await websocket.recv()
    event = json.loads(message)
    assert event["type"] == "init"

    if "emitter" in event:
        await join_emitters(
            websocket=websocket,
            emitter_key=event["emitter"],
            receiver_key=event["receiver"],
        )
    if "receiver" in event:
        await join_receivers(websocket=websocket, receiver_key=event["receiver"])
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
