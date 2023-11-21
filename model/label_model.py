from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from assiatant import GB

Base = declarative_base()


class LabelModel(Base):
    __tablename__ = 'label'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    sort = Column(Integer, default=0)
