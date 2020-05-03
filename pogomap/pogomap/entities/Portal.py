from dataclasses import dataclass

from .Entity import Entity


@dataclass
class Portal(Entity):
    type: str = "portal"
