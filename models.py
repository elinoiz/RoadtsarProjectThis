from sqlalchemy import Column, Integer, String, ForeignKey, BLOB, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(50), unique=True, index=True)
    user_pass = Column(String(50))
    photo = Column(BLOB)

    ads = relationship("Advertisement", back_populates="owner")
    bids = relationship("Bid", back_populates="user")

class Advertisement(Base):
    __tablename__ = "emadvertisents"

    ad_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    city = Column(String(255))
    description = Column(String(3000))
    start_price = Column(Integer)
    title = Column(String(25))
    category = Column(String(50))
    photo = Column(LargeBinary, nullable=True)

    owner = relationship("User", back_populates="ads")
    bids = relationship("Bid", back_populates="advertisement")

class Bid(Base):
    __tablename__ = 'bids'

    bid_id = Column(Integer, primary_key=True, autoincrement=True)
    ad_id = Column(Integer, ForeignKey('emadvertisents.ad_id'))
    user_id = Column(Integer, ForeignKey('users.user_id'))
    bid_amount = Column(Integer)

    advertisement = relationship("Advertisement", back_populates="bids")
    user = relationship("User", back_populates="bids")
