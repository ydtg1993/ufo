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
    chapter_count = Column(Integer, default=0)
    is_finish = Column(Integer, default=0)
    description = Column(String, default='')
    status = Column(Integer, default=0)
    last_chapter_update_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

    @classmethod
    def insert(cls) -> int:
        i = 0
        try:
            comic = cls(
                title=cls.title,
                source_url=cls.source_url,
                source=cls.source,
                cover=cls.cover,
                region=cls.region,
                category=cls.category,
                label=cls.label,
                is_finish=cls.is_finish,
                description=cls.description,
                author=cls.author
            )
            GB.mysql.session.add(comic)
            GB.mysql.session.commit()
            i = comic.id
        except Exception as e:
            print(f"Database error: {e}")
            GB.mysql.reconnect()

        return i