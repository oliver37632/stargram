from src.model import Base

from sqlalchemy import Column, BINARY, VARCHAR
from sqlalchemy_utils import UUIDType


class UserTbl(Base):
        __tablename__ = 'user_tbl'

        id = Column(UUIDType(binary=True), primary_key=True, )
        account_id = Column(VARCHAR(10), nullable=False)
        email = Column(VARCHAR(320), nullable=False)
        password = Column(VARCHAR(256), nullable=False)
