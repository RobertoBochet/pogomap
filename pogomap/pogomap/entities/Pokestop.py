from dataclasses import dataclass

from .Entity import Entity


@dataclass
class Pokestop(Entity):
    type: str = "pokestop"
