from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Portal(Base):
    __tablename__ = "portals"

    id = Column("id", Integer, primary_key=True)
    latitude = Column("latitude", Float)
    longitude = Column("longitude", Float)
    name = Column("name", String)
    image = Column("image", String)
    guid = Column("guid", String)
