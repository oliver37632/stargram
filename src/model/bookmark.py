from src.model import Base

from sqlalchemy import Column, BigInteger, ForeignKey
from sqlalchemy.orm import relationship


class BookmarkTbl(Base):
    __tablename__ = 'bookmark_tbl'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(ForeignKey('user_tbl.id', ondelete='CASCADE'), nullable=False, index=True)
    feed_id = Column(ForeignKey('feed_tbl.id', ondelete='CASCADE'), nullable=False, index=True)

    feed = relationship('FeedTbl')
    user = relationship('UserTbl')
