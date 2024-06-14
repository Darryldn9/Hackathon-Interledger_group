from sqlalchemy.orm import Session
import models, schemas
from datetime import datetime, date

def get_subscriptions(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Subscription).offset(skip).limit(limit).all()

def get_subscription(db: Session, subscription_id: int):
    return db.query(models.Subscription).filter(models.Subscription.id == subscription_id).first()

def create_subscription(db: Session, subscription: schemas.SubscriptionCreate):
    db_subscription = models.Subscription(**subscription.dict(), payment_date=None)
    db.add(db_subscription)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription

def update_subscription(db: Session, subscription_id: int, subscription: schemas.SubscriptionUpdate):
    db_subscription = db.query(models.Subscription).filter(models.Subscription.id == subscription_id).first()
    if db_subscription is None:
        return None
    for key, value in subscription.dict().items():
        setattr(db_subscription, key, value)
    db.commit()
    db.refresh(db_subscription)
    return db_subscription

def make_payment(db: Session, subscription_id: int):
    db_subscription = db.query(models.Subscription).filter(models.Subscription.id == subscription_id).first()
    if db_subscription is None:
        return None
    db_subscription.status = "paid"
    db_subscription.payment_date = datetime.utcnow()
    db.commit()
    db.refresh(db_subscription)
    return db_subscription

def get_days_until_next_repayment(subscription: models.Subscription) -> int:
    today = date.today()
    repayment_day = int(subscription.repayment_date)
    if today.day <= repayment_day:
        next_repayment_date = date(today.year, today.month, repayment_day)
    else:
        next_repayment_date = date(today.year, today.month + 1 if today.month < 12 else 1, repayment_day)

    days_until_next_repayment = (next_repayment_date - today).days
    return days_until_next_repayment

def get_accounts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Account).offset(skip).limit(limit).all()

def create_account(db: Session, account: schemas.AccountCreate):
    db_account = models.Account(**account.dict())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

def connect_account(db: Session, account_id: int):
    db_account = db.query(models.Account).filter(models.Account.id == account_id).first()
    if db_account is None:
        return None
    # Logic for connecting the account (e.g., setting a flag, updating status, etc.)
    # Here, we'll just print a message to simulate the connection
    print(f"Account {db_account.account_name} connected!")
    return db_account
