import json
from constants import *

async def Error(websocket, message):
    event = {
        METHOD: FROM_SERVER,
        OBJECT: OBJECT_INFO,
        DATA_INFO_TYPE: DATA_INFO_TYPE_ERROR,
        DATA_INFO_TYPE_ERROR: message
    }
    if websocket.closed:
        return
    await websocket.send(json.dumps(event))

async def ToAll(dumped_message, connected):
    # websockets.broadcast(connected, dumped_message)
    for c in connected:
        if c.ws.closed:
            return
        await c.ws.send(dumped_message)
