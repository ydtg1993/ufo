from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
Base = declarative_base()


class NewModel(Base):
    __tablename__ = 'media'
    media_id = Column(Integer, primary_key=True)
    title = Column(String)
    cover = Column(String)
    full_title = Column(String)
    content = Column(String)
    introduce = Column(String)
    category_id = Column(Integer)
    source_id = Column(Integer)
    source_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
