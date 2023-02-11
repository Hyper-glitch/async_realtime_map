import trio
from trio_websocket import serve_websocket

from server import server


async def main():
    await serve_websocket(server, '127.0.0.1', 8000, ssl_context=None)

if __name__ == '__main__':
    trio.run(async_fn=main)
