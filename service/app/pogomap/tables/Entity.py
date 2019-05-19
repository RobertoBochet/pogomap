from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Entity(Base):
    __tablename__ = "entities"

    id = Column("id", Integer, primary_key=True)
    type = Column("type", String)
    is_eligible = Column("is_eligible", Boolean)
