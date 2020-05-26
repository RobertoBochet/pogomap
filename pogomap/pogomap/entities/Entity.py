from dataclasses import dataclass


@dataclass
class Entity:
    id: int
    name: str
    latitude: float
    longitude: float
    image: str
    type: str
    is_eligible: bool = False

    def get_image(self) -> str:
        return "" if self.image == "" else "//" + self.image.split("//")[1]
