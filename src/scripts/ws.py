#!/usr/bin/env python

import logging
logger = logging.getLogger('websockets')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

import asyncio
import django
import websockets

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

django.setup()

from django.core.management import call_command

from sesame.utils import get_user
from websockets.frames import CloseCode

async def handler(websocket):
    sesame = await websocket.recv()
    user = await asyncio.to_thread(get_user, sesame)
    if user is None:
        await websocket.close(CloseCode.INTERNAL_ERROR, "authentication failed")
        return

    await websocket.send(f"Hello {user}!")


async def main():
    async with websockets.serve(handler, "0.0.0.0", 8888):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())