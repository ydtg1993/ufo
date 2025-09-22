import json

from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Index
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime


Base = declarative_base()


class SourceImageModel(Base):
    __tablename__ = 'source_image'

    id = Column(Integer, primary_key=True, autoincrement=True)
    comic_id = Column(Integer, nullable=False, default=0)
    chapter_id = Column(Integer, nullable=False)
    images = Column(Text, nullable=False)  # 使用 Text 存储 JSON 字符串
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    created_at = Column(DateTime, nullable=False, default=datetime.now)

    __table_args__ = (
        Index('chapter_id', 'chapter_id', unique=True),
        Index('comic_id', 'comic_id'),
        {'comment': '采集-漫画图片'}
    )

    def set_images(self, images_list):
        """设置images为JSON字符串"""
        self.images = json.dumps(images_list, ensure_ascii=False)

    def get_images(self):
        """获取解析后的images列表"""
        if self.images:
            return json.loads(self.images)
        return []
