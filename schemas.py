from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SubscriptionBase(BaseModel):
    name: str
    payment_amount: int
    repayment_date: str  # Accept only the day
    payment_pointer: Optional[str] = None

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionUpdate(SubscriptionBase):
    payment_date: Optional[datetime] = None
    status: str

class Subscription(SubscriptionBase):
    id: int
    payment_date: Optional[datetime] = None
    status: str
    account_id: Optional[int] = None

    class Config:
        orm_mode = True

class AccountBase(BaseModel):
    account_name: str
    account_type: str

class AccountCreate(AccountBase):
    pass

class Account(AccountBase):
    id: int
    subscriptions: list[Subscription] = []

    class Config:
        orm_mode = True
