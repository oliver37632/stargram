from src.model import Base

from sqlalchemy import Column, BigInteger, ForeignKey, VARCHAR, TIMESTAMP, text
from sqlalchemy.orm import relationship


class CommentTbl(Base):
    __tablename__ = 'comment_tbl'

    id = Column(BigInteger, primary_key=True)
    user_id = Column(ForeignKey('user_tbl.id', ondelete='CASCADE'), nullable=False, index=True)
    feed_id = Column(ForeignKey('feed_tbl.id', ondelete='CASCADE'), nullable=False, index=True)
    content = Column(VARCHAR(255), nullable=False)
    create_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    feed = relationship('FeedTbl')
    user = relationship('UserTbl')