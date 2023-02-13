from sys import stderr

import trio
from trio_websocket import open_websocket_url

from dto import RouteDTO, BusDTO
from route_helper import load_routes


def generate_bus_id(route_id, bus_index):
    return f"{route_id}-{bus_index}"


async def run_bus(route, route_dto, idx):
    bus_id = generate_bus_id(route_id=route_dto.name, bus_index=generate_bus_id(route_id=route_dto.name, bus_index=idx))
    async with open_websocket_url("ws://127.0.0.1:8080") as ws:
        for lat, lng in route:
            bus_dto = BusDTO(busId=bus_id, lat=lat, lng=lng, route=route_dto.name)
            await ws.send_message(bus_dto.json())
            await trio.sleep(3)


async def fake_bus_client():
    try:
        async with trio.open_nursery() as nursery:
            for route in load_routes():
                route_dto = RouteDTO(**route)
                middle_route_index = len(route_dto.coordinates) / 2
                start_middle_path = route_dto.coordinates[:round(middle_route_index)]
                end_middle_path = route_dto.coordinates[round(middle_route_index):]
                paths = [start_middle_path, end_middle_path]
                for idx, path in enumerate(paths):
                    nursery.start_soon(run_bus, path, route_dto, idx)

    except OSError as ose:
        print('Connection attempt failed: %s' % ose, file=stderr)


if __name__ == '__main__':
    while True:
        trio.run(async_fn=fake_bus_client)
