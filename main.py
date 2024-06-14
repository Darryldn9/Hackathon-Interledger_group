from fastapi import FastAPI, Depends, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine
import logging
from datetime import datetime

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

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
        for subscription in subscriptions:
            subscription.days_until_next_repayment = crud.get_days_until_next_repayment(subscription)
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
    repayment_date: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        subscription = schemas.SubscriptionCreate(
            name=name,
            payment_amount=payment_amount,
            repayment_date=repayment_date
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
    payment_date: str = Form(None),
    repayment_date: str = Form(...),
    status: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        payment_date = datetime.strptime(payment_date, "%Y-%m-%d") if payment_date else None
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

@app.post("/subscriptions/pay/{subscription_id}")
def pay_subscription(subscription_id: int, db: Session = Depends(get_db)):
    try:
        crud.make_payment(db=db, subscription_id=subscription_id)
        return RedirectResponse(url="/subscriptions/", status_code=303)
    except Exception as e:
        logging.error(f"Error making payment for subscription: {e}")
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
def add_account(account_name: str = Form(...), account_type: str = Form(...), db: Session = Depends(get_db)):
    try:
        account = schemas.AccountCreate(account_name=account_name, account_type=account_type)
        crud.create_account(db=db, account=account)
        return RedirectResponse(url="/accounts/", status_code=303)
    except Exception as e:
        logging.error(f"Error adding account: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/accounts/connect/{account_id}")
def connect_account(account_id: int, db: Session = Depends(get_db)):
    try:
        crud.connect_account(db=db, account_id=account_id)
        return RedirectResponse(url="/accounts/", status_code=303)
    except Exception as e:
        logging.error(f"Error connecting account: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
