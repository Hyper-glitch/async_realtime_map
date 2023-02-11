from pydantic import BaseModel


class BusDTO(BaseModel):
    busId: str
    lat: float
    lng: float
    route: str


class BusCoordinatesDTO(BaseModel):
    lat: float
    lng: float


class RouteDTO(BaseModel):
    name: str
    station_start_name: str
    station_stop_name: str
    coordinates: list[list[float]]
    stations: list


class WindowCoordinatesDTO(BaseModel):
    south_lat: float
    north_lat: float
    west_lng: float
    east_lng: float


class ServerMessageDTO(BaseModel):
    msgType: str
    buses: list[BusDTO]


class ClientMessageDTO(BaseModel):
    msgType: str
    data: WindowCoordinatesDTO
