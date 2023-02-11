import json

import aiofiles

from dto import RouteDTO


async def read_route_file():
    async with aiofiles.open('routes/156.json', mode='r') as file:
        content = await file.read()
    route = json.loads(content)
    route_dto = RouteDTO(**route)
    return route_dto
