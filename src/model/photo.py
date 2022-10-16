from src.model import Base

from sqlalchemy import Column, BigInteger, ForeignKey, VARCHAR
from sqlalchemy.orm import relationship


class PhotoTbl(Base):
    __tablename__ = 'photo_tbl'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    feed_id = Column(ForeignKey('feed_tbl.id', ondelete='CASCADE'), nullable=False, index=True)
    url = Column(VARCHAR(300), nullable=False)

    feed = relationship('FeedTbl')
