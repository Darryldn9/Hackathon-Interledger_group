from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SubscriptionBase(BaseModel):
    name: str
    payment_amount: int
    payment_date: datetime
    repayment_date: datetime
    status: str

class SubscriptionCreate(SubscriptionBase):
    pass

class SubscriptionUpdate(SubscriptionBase):
    pass

class Subscription(SubscriptionBase):
    id: int
    account_id: Optional[int] = None

    class Config:
        orm_mode = True

class AccountBase(BaseModel):
    account_type: str
    balance: int

class AccountCreate(AccountBase):
    pass

class Account(AccountBase):
    id: int
    subscriptions: list[Subscription] = []

    class Config:
        orm_mode = True
