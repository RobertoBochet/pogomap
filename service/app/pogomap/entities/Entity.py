from dataclasses import dataclass, asdict


@dataclass
class Entity:
    id: int
    name: str
    latitude: float
    longitude: float
    image: str
    guid: str
    type: str
    is_eligible: bool = False
