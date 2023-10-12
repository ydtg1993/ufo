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

    @classmethod
    def insert(cls) -> int:
        i = 0
        try:
            news = cls(
                title=cls.title,
                cover=cls.cover,
                full_title=cls.full_title,
                source_url=cls.link,
                introduce=cls.introduce,
                source_id=cls.source_id,
                categories=cls.categories,
                publish_at=cls.publish_at
            )
            GB.mysql.session.add(news)
            GB.mysql.session.commit()
            i = news.media_id
        except Exception as e:
            print(f"Database error: {e}")
            GB.mysql.reconnect()
        return i
