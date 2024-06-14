from fastapi import FastAPI, Depends, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine

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
    subscriptions = crud.get_subscriptions(db)
    return templates.TemplateResponse("index.html", {"request": request, "subscriptions": subscriptions})

@app.get("/subscriptions/")
def read_subscriptions(request: Request, db: Session = Depends(get_db)):
    subscriptions = crud.get_subscriptions(db)
    return templates.TemplateResponse("subscriptions.html", {"request": request, "subscriptions": subscriptions})

@app.get("/subscriptions/add/")
def add_subscription_form(request: Request):
    return templates.TemplateResponse("add_subscription.html", {"request": request})

@app.post("/subscriptions/add/")
def add_subscription(name: str = Form(...), payment_amount: int = Form(...), db: Session = Depends(get_db)):
    subscription = schemas.SubscriptionCreate(name=name, payment_amount=payment_amount)
    crud.create_subscription(db=db, subscription=subscription)
    return RedirectResponse(url="/subscriptions/", status_code=303)
