from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from assiatant import GB

Base = declarative_base()


class SourceVideoModel(Base):
    __tablename__ = 'source_video'
    id = Column(Integer, primary_key=True)
    source_url = Column(String)
    title = Column(String)
    cover = Column(String, default='')
    big_cover = Column(String, default='')
    url = Column(String, default='')
    label = Column(String, default='[]')
    status = Column(Integer, default=0)
    like = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
