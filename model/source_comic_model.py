from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from assiatant import GB

Base = declarative_base()


class SourceComicModel(Base):
    __tablename__ = 'source_comic'
    id = Column(Integer, primary_key=True)
    source_url = Column(String)
    source = Column(Integer, default=0)
    title = Column(String)
    author = Column(String, default='')
    cover = Column(String, default='')
    label = Column(String, default='[]')
    category = Column(String, default='')
    region = Column(String, default='')
    source_chapter_count = Column(Integer, default=0)
    chapter_count = Column(Integer, default=0)
    is_finish = Column(Integer, default=0)
    description = Column(String, default='')
    status = Column(Integer, default=0)
    last_chapter_update_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)