import json
import logging
import random
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from assiatant import GB
from model.label_model import LabelModel
from model.source_video_model import SourceVideoModel
from model.video_label_ass_model import VideoLabelAssModel
from model.video_model import VideoModel


class TransVideo:
    target_session = None
    label_hash = {}

    def __init__(self):
        try:
            db = GB.config.get("Database", "DB")
            engine = create_engine(
                f"mysql+mysqlconnector://YDTG1993:Pierkadan.6603!93@47.245.100.156:3306/{db}")
            engine.connect()
            sessionCls = sessionmaker(bind=engine)
            self.target_session = sessionCls()
            self.exec()
        except BaseException as e:
            print(f'{e}')

    def exec(self):
        session = GB.mysql.connect()
        try:
            results = session.query(SourceVideoModel).filter(
                and_(
                    SourceVideoModel.url != '',
                    SourceVideoModel.status == 0
                )
            ).offset(0).limit(random.randint(3, 15)).all()
            self.get_all_label()
            for record in results:
                labels = json.loads(record.label)
                label_ids = []
                for _, label in enumerate(labels):
                    if label in self.label_hash:
                        label_ids.append(self.label_hash[label])
                    else:
                        lid = self.insert_label(label)
                        label_ids.append(lid)
                if self.target_session.query(VideoModel).filter(
                        VideoModel.source_url == record.source_url).first() is not None:
                    continue
                video = VideoModel(
                    title=record.title,
                    source_id=record.id,
                    source_url=record.source_url,
                    cover=record.cover,
                    like=record.like,
                    url=record.url,
                    big_cover=record.big_cover,
                )
                self.target_session.add(video)
                self.target_session.flush()
                self.insert_label_ass(video.id, label_ids)
                session.query(SourceVideoModel).filter(SourceVideoModel.id == record.id).update({
                    SourceVideoModel.status: 1})
            self.target_session.commit()
            session.commit()
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception(str(e))
        finally:
            session.close()
        pass

    def insert_label_ass(self, vid, lids):
        if len(lids) == 0:
            return
        ass = []
        for _, lid in enumerate(lids):
            ass.append(VideoLabelAssModel(label_id=lid, video_id=vid))
        self.target_session.bulk_save_objects(ass)

    def insert_label(self, name) -> int:
        label = LabelModel(name=name)
        self.target_session.add(label)
        self.target_session.flush()
        self.label_hash[name] = label.id
        return label.id

    def get_all_label(self):
        results = self.target_session.query(LabelModel).all()
        for record in results:
            self.label_hash[record.name] = record.id
