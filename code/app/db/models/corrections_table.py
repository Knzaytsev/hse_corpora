from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
import uuid

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Corrections(Base):
    __tablename__ = "corrections"

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    mistake_id = Column(Integer)
    text_id = Column(Integer)
    sentence_id = Column(Integer)
    correction_token_id = Column(Integer)
    correction_token = Column(String)
    correction_pos = Column(String)
    correction_lemma = Column(String)
    first_token_id = Column(String)
    correction_start_inx = Column(Integer)
