from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from assiatant import GB

Base = declarative_base()


class VideoLabelAssModel(Base):
    __tablename__ = 'video_label_ass'
    id = Column(Integer, primary_key=True)
    label_id = Column(Integer, default=0)
    video_id = Column(Integer, default=0)
