#!/usr/bin/env python3

import asyncio
import websockets
import json

async def hello(websocket, path):
    with open("./menu.json") as f:
        await websocket.send(f.read())
    with open("./example.json") as f:
        data = json.load(f)
        for message in data:
            await websocket.send(json.dumps({"message":message}))
            await asyncio.sleep(1)

    command = None
    while(command != "quit"): 
        command = await websocket.recv()
        print("Receive: {}".format(command))
    websocket.close()
    exit()

start_server = websockets.serve(hello, 'localhost', 3000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
