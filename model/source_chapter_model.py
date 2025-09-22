from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Index
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from assiatant import GB

Base = declarative_base()


class SourceChapterModel(Base):
    __tablename__ = 'source_chapter'

    id = Column(Integer, primary_key=True, autoincrement=True)
    comic_id = Column(Integer, nullable=False)
    source_url = Column(String(500), nullable=False, default='', comment='源url')
    cover = Column(String(500), nullable=False, default='', comment='封面')
    title = Column(String(500), nullable=False, default='', comment='标题')
    sort = Column(Integer, nullable=False, default=0)
    status = Column(Integer, nullable=False, default=0, comment='0未审核 1通过')
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

    __table_args__ = (
        Index('source_unique', 'comic_id', 'source_url', unique=True),
        Index('comic_id', 'comic_id'),
        {'comment': '采集-漫画章节'}
    )
