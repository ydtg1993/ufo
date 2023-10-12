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

    def insert(self) -> int:
        i = 0
        try:
            news = NewModel(
                title=self.title,
                cover=self.cover,
                full_title=self.full_title,
                source_url=self.source_url,
                introduce=self.introduce,
                source_id=self.source_id,
                categories=self.categories,
                publish_at=self.publish_at
            )
            GB.mysql.session.add(news)
            GB.mysql.session.commit()
            i = news.media_id
        except Exception as e:
            print(f"Database error: {e}")
            GB.mysql.reconnect()
        return i
