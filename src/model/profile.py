from src.model import Base
from src.model.user import UserTbl
from sqlalchemy import Column, ForeignKey, VARCHAR, BINARY

from sqlalchemy.orm import relationship

class ProfileTbl(Base):
    __tablename__ = 'profile_tbl'

    name = Column(VARCHAR(5), primary_key=True)
    introduce = Column(VARCHAR(30), nullable=False)
    photo = Column(VARCHAR(300), nullable=False)
    link = Column(VARCHAR(255))
    id = Column(ForeignKey('user_tbl.id', ondelete='CASCADE'), nullable=False, index=True)

    user_tbl = relationship('UserTbl')

