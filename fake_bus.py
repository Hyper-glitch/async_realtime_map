from sys import stderr

import trio
from trio_websocket import open_websocket_url

from dto import RouteDTO, BusDTO
from route_helper import load_routes


async def run_bus(route):
    async with open_websocket_url("ws://127.0.0.1:8080") as ws:
        route_dto = RouteDTO(**route)
        for lat, lng in route_dto.coordinates:
            bus_dto = BusDTO(busId=route_dto.name, lat=lat, lng=lng, route=route_dto.name)
            await ws.send_message(bus_dto.json())
            await trio.sleep(3)


async def fake_bus_client():
    try:
        async with trio.open_nursery() as nursery:
            for route in load_routes():
                nursery.start_soon(run_bus, route)
    except OSError as ose:
        print('Connection attempt failed: %s' % ose, file=stderr)


if __name__ == '__main__':
    while True:
        trio.run(async_fn=fake_bus_client)
