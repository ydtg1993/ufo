from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CateModel(Base):
    __tablename__ = 'media_category'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    @staticmethod
    def get_or_create_id_by_name(session, name):
        existing_category = session.query(CateModel).filter_by(name=name).first()

        if existing_category:
            return existing_category.id
        else:
            category = CateModel(name=name)
            session.add(category)
            session.commit()
            return category.id