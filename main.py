from functools import partial

import trio
from trio_websocket import serve_websocket

from server import server, send_to_browser


async def main():
    async with trio.open_nursery() as nursery:
        partial_server = partial(serve_websocket, server, host='127.0.0.1', port=8080, ssl_context=None)
        partial_send_to_browser = partial(
            serve_websocket,
            send_to_browser,
            host='127.0.0.1',
            port=8000,
            ssl_context=None,
        )
        nursery.start_soon(partial_server)
        nursery.start_soon(partial_send_to_browser)


if __name__ == '__main__':
    trio.run(async_fn=main)
