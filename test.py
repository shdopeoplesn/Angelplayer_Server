#!/usr/bin/env python

# WS server example

import asyncio
import websockets

async def hello(websocket, path):
    loop = asyncio.get_event_loop()

start_server = websockets.serve(hello, "localhost", 7779)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()