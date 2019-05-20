from dataclasses import dataclass

from .Entity import Entity


@dataclass
class Unverified(Entity):
    type: str = "unverified"
