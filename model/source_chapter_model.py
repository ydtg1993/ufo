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

    def insert(self) -> int:
        i = 0
        try:
            chapter = SourceChapterModel(
                title=self.title,
                comic_id=self.comic_id,
                images=self.images,
                source_url=self.source_url,
                sort=self.sort
            )
            GB.mysql.session.add(chapter)
            GB.mysql.session.commit()
            i = chapter.id
        except Exception as e:
            print(f"Database error: {e}")
            GB.mysql.reconnect()

        return i
