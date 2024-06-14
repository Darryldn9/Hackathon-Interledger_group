from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SubscriptionBase(BaseModel):
    name: str
    payment_amount: int
    repayment_date: str  # Accept month and day only

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionUpdate(SubscriptionBase):
    payment_date: datetime
    status: str

class Subscription(SubscriptionBase):
    id: int
    payment_date: datetime
    status: str
    account_id: Optional[int] = None

    class Config:
        orm_mode = True

class AccountBase(BaseModel):
    account_name: str
    account_type: str
    balance: int

class AccountCreate(AccountBase):
    pass

class Account(AccountBase):
    id: int
    subscriptions: list[Subscription] = []

    class Config:
        orm_mode = True
