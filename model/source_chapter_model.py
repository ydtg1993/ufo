from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from assiatant import GB

Base = declarative_base()


class SourceChapterModel(Base):
    __tablename__ = 'source_chapter'
    id = Column(Integer, primary_key=True)
    comic_id = Column(Integer, default=0)
    source_url = Column(String)
    title = Column(String)
    images = Column(String)
    img_count = Column(Integer, default=0)
    sort = Column(Integer, default=0)
    status = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
