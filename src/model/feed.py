from src.model import Base

from sqlalchemy import Column, VARCHAR, BINARY, ForeignKey, Integer, TIMESTAMP, text
from sqlalchemy.orm import relationship


class FeedTbl(Base):
    __tablename__ = 'feed_tbl'

    id = Column(BINARY(16), primary_key=True)
    user_id = Column(ForeignKey('user_tbl.id', ondelete='CASCADE'), nullable=False, index=True)
    title = Column(VARCHAR(30), nullable=False)
    content = Column(VARCHAR(255), nullable=False)
    create_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    category = Column(VARCHAR(10), nullable=False)
    heart_count = Column(Integer)
    comment_count = Column(Integer)

    user = relationship('UserTbl')