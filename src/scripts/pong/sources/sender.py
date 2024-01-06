import asyncio
import websockets
import json
from constants import *

async def Error(websocket, message):
    event = {
        METHOD: FROM_SERVER,
        OBJECT: OBJECT_INFO,
        DATA_INFO_TYPE: DATA_INFO_TYPE_ERROR,
        DATA_INFO_TYPE_ERROR: message
    }
    await websocket.send(json.dumps(event))

async def ToAll(dumped_message, connected):
    # websockets.broadcast(connected, dumped_message)
    for ws in connected:
        await ws.send(dumped_message)
