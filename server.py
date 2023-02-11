from pydantic.error_wrappers import ValidationError
from trio_websocket import ConnectionClosed

from dto import ClientMessageDTO, BusDTO


async def server(request):
    ws = await request.accept()
    while True:
        dto = None
        message = await ws.get_message()
        try:
            dto = BusDTO.parse_raw(message)
        except ValidationError:
            dto = ClientMessageDTO.parse_raw(message)
        except ConnectionClosed:
            break
        finally:
            print(dto)
