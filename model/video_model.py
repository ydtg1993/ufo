from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from assiatant import GB

Base = declarative_base()


class VideoModel(Base):
    __tablename__ = 'video'
    id = Column(Integer, primary_key=True)
    source_id = Column(Integer)
    source_url = Column(String)
    title = Column(String)
    cover = Column(String, default='')
    big_cover = Column(String, default='')
    url = Column(String, default='')
    like = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
