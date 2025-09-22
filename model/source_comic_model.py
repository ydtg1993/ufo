from sqlalchemy import Column, Integer, String, DateTime, JSON, Boolean, Index, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from assiatant import GB

Base = declarative_base()


class SourceComicModel(Base):
    __tablename__ = 'source_comic'
    id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(Integer, nullable=False, default=1, comment='采集源 1:快看 2:腾讯')
    source_url = Column(String(255), nullable=False, default='', comment='源url')
    cover = Column(String(255), nullable=False, default='', comment='封面')
    title = Column(String(255), nullable=False, default='', comment='标题')
    author = Column(String(255), nullable=False, default='', comment='作者')
    label = Column(JSON, nullable=False, comment='标签')
    category = Column(String(255), nullable=False, comment='分类')
    region = Column(String(255), nullable=False, default='', comment='地区')
    chapter_count = Column(Integer, nullable=False, default=0, comment='章节数量')
    chapter_count_download = Column(Integer, nullable=False, default=0, comment='章节数量(已下载)')
    like = Column(String(255), nullable=False, default='', comment='喜欢')
    popularity = Column(String(255), nullable=False, default='0', comment='人气热度')
    is_finish = Column(Boolean, nullable=False, default=False, comment='0连载 1完结')
    description = Column(String(500), nullable=False, default='', comment='描述')
    status = Column(Integer, nullable=False, default=0, comment='0未审核 1通过')
    last_chapter_update_at = Column(DateTime, nullable=False, default=datetime.now, comment='最新章节更新时间')
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

    __table_args__ = (
        Index('source_url', 'source_url', unique=True),
        Index('status', 'status'),
        Index('category', 'category'),
        Index('finish', 'is_finish'),
        {'comment': '采集-漫画'}
    )
