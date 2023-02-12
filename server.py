import trio
from pydantic.error_wrappers import ValidationError
from trio_websocket import ConnectionClosed

from dto import ClientMessageDTO, BusDTO, ServerMessageDTO

BUSES: list[BusDTO] = []


async def server(request):
    ws = await request.accept()
    while True:
        dto = None
        message = await ws.get_message()
        try:
            dto = BusDTO.parse_raw(message)
            BUSES.append(dto)
        except ValidationError:
            dto = ClientMessageDTO.parse_raw(message)
        except (ConnectionClosed, BaseException):
            break
        finally:
            print(dto)


async def send_to_browser(request):
    ws = await request.accept()
    while True:
        server_msg_dto = ServerMessageDTO(msgType="Buses", buses=BUSES)
        try:
            await ws.send_message(server_msg_dto.json())
            await trio.sleep(1)
        except (ConnectionClosed, BaseException):
            break
