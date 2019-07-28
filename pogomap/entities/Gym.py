from dataclasses import dataclass

from .Entity import Entity


@dataclass
class Gym(Entity):
    type: str = "gym"
