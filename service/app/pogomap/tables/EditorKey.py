from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class EditorKey(Base):
    __tablename__ = "editorkeys"

    key = Column(String(32), primary_key=True)
    comment = Column(String)
