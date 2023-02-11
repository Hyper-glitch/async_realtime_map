import json
from sys import stderr

import trio
from trio_websocket import open_websocket_url

from dto import RouteDTO, BusDTO


async def fake_bus_client():
    try:
        async with open_websocket_url("ws://127.0.0.1:8000") as ws:
            with open('routes/156.json', mode='r') as file:
                content = file.read()
            route = json.loads(content)
            route_dto = RouteDTO(**route)
            for lat, lng in route_dto.coordinates:
                bus_dto = BusDTO(busId="c790с", lat=lat, lng=lng, route="156")
                await ws.send_message(bus_dto.json())
                await trio.sleep(3)
    except OSError as ose:
        print('Connection attempt failed: %s' % ose, file=stderr)


if __name__ == '__main__':
    trio.run(async_fn=fake_bus_client)
