from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    payment_amount = Column(Integer)
    payment_date = Column(DateTime, default=datetime.datetime.utcnow)
    repayment_date = Column(String, default="01-01")  # Default to January 1st
    status = Column(String, default="unpaid")
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=True)

    account = relationship("Account", back_populates="subscriptions")

class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    account_name = Column(String)
    account_type = Column(String)
    balance = Column(Integer)

    subscriptions = relationship("Subscription", back_populates="account")
