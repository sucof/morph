#! /user/bin/python
# coding:UTF-8

import asyncio

import config
from core import websockets

@asyncio.coroutine
def websocketHandle(websocket, path):
    while True:
        if not websocket.open:
            return
        msg = yield from websocket.recv()
        if msg is None:
            continue
        # 记录当前最近的VECTOR样本序号
        config.MOR_LAST_COMPLETE_VECOTR = int(msg)
        yield from websocket.send('OK')

def Run(ws_host, ws_port):
    ws_server = websockets.serve(websocketHandle, ws_host, ws_port)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(ws_server)
    loop.run_forever()