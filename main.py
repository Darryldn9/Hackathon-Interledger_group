from fastapi import FastAPI, Depends, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine
import logging
from datetime import datetime

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root(request: Request, db: Session = Depends(get_db)):
    try:
        subscriptions = crud.get_subscriptions(db)
        return templates.TemplateResponse("index.html", {"request": request, "subscriptions": subscriptions})
    except Exception as e:
        logging.error(f"Error fetching root data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/subscriptions/")
def read_subscriptions(request: Request, db: Session = Depends(get_db)):
    try:
        subscriptions = crud.get_subscriptions(db)
        return templates.TemplateResponse("subscriptions.html", {"request": request, "subscriptions": subscriptions})
    except Exception as e:
        logging.error(f"Error fetching subscriptions data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/subscriptions/add/")
def add_subscription_form(request: Request):
    return templates.TemplateResponse("add_subscription.html", {"request": request})

@app.post("/subscriptions/add/")
def add_subscription(
    name: str = Form(...),
    payment_amount: int = Form(...),
    payment_date: str = Form(...),
    repayment_date: str = Form(...),
    status: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        payment_date = datetime.strptime(payment_date, "%Y-%m-%d")
        repayment_date = datetime.strptime(repayment_date, "%Y-%m-%d")
        subscription = schemas.SubscriptionCreate(
            name=name,
            payment_amount=payment_amount,
            payment_date=payment_date,
            repayment_date=repayment_date,
            status=status
        )
        crud.create_subscription(db=db, subscription=subscription)
        return RedirectResponse(url="/subscriptions/", status_code=303)
    except Exception as e:
        logging.error(f"Error adding subscription: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/subscriptions/edit/{subscription_id}")
def edit_subscription_form(subscription_id: int, request: Request, db: Session = Depends(get_db)):
    try:
        subscription = crud.get_subscription(db, subscription_id=subscription_id)
        if subscription is None:
            raise HTTPException(status_code=404, detail="Subscription not found")
        return templates.TemplateResponse("edit_subscription.html", {"request": request, "subscription": subscription})
    except Exception as e:
        logging.error(f"Error fetching subscription data for editing: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/subscriptions/edit/{subscription_id}")
def edit_subscription(
    subscription_id: int,
    name: str = Form(...),
    payment_amount: int = Form(...),
    payment_date: str = Form(...),
    repayment_date: str = Form(...),
    status: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        payment_date = datetime.strptime(payment_date, "%Y-%m-%d")
        repayment_date = datetime.strptime(repayment_date, "%Y-%m-%d")
        subscription = schemas.SubscriptionUpdate(
            name=name,
            payment_amount=payment_amount,
            payment_date=payment_date,
            repayment_date=repayment_date,
            status=status
        )
        crud.update_subscription(db=db, subscription_id=subscription_id, subscription=subscription)
        return RedirectResponse(url="/subscriptions/", status_code=303)
    except Exception as e:
        logging.error(f"Error editing subscription: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/accounts/")
def read_accounts(request: Request, db: Session = Depends(get_db)):
    try:
        accounts = crud.get_accounts(db)
        return templates.TemplateResponse("accounts.html", {"request": request, "accounts": accounts})
    except Exception as e:
        logging.error(f"Error fetching accounts data: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/accounts/add/")
def add_account_form(request: Request):
    return templates.TemplateResponse("add_account.html", {"request": request})

@app.post("/accounts/add/")
def add_account(account_type: str = Form(...), balance: int = Form(...), db: Session = Depends(get_db)):
    try:
        account = schemas.AccountCreate(account_type=account_type, balance=balance)
        crud.create_account(db=db, account=account)
        return RedirectResponse(url="/accounts/", status_code=303)
    except Exception as e:
        logging.error(f"Error adding account: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
