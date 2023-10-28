from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from assiatant import GB

Base = declarative_base()


class NewModel(Base):
    __tablename__ = 'source_media'
    media_id = Column(Integer, primary_key=True)
    title = Column(String)
    cover = Column(String)
    full_title = Column(String)
    introduce = Column(String)
    categories = Column(String)
    source_id = Column(Integer)
    source_url = Column(String)
    publish_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
