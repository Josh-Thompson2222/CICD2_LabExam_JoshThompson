# app/main.py
from typing import Optional

from contextlib import asynccontextmanager
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import engine, SessionLocal
from app.models import Base
#from app.schemas import 

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup (dev/exam). Prefer Alembic in production.
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()


# ---- Health ----
@app.get("/health")
def health():
    return {"status": "ok"}


# ---- Customers ----
@app.post("/api/customers", response_model = UserRead, status_code =status.HTTP_201_CREATED)
def add_customer(payload: CustomerCreate, db: Session = Depends(get_db)):
    customer=CustomerDB(**payload.model_dump())
    db.add(customer)
        try:
            db.commit()
            db.refresh(customer)
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code = 409, detail = "Customer already exists")
        return customer

@app.get ("/api/customers", response_model = list[CustomerRead])
def list_customers(db: Session = Depends(get_db)):
    stmt = select (UserDB).order_by(UserDB.id)
    return list (db.execute(stmt).scalars())

@app.get ("/api/customers/{customer_id}", response_model=CustomerRead)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer= db.get(CustomerDB, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail = "Customer not found")
    return customer

@app.put ("api/customers/{customer_id}", status_code = status.HTTP_200_OK)
def update_customer(customer_id: int, updated_customer: Customer)
    for i, u in enumerate(Customer):
        if u.customer_id = customer_id:
            customers[i] = updated_customer
            return updated_customer
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f("Customer with ID {customer_id} already exists"))

@app.patch ("/api/customers/{customer_id}")
def test_patch_customer(customer_id: int, partial_customer: dict)
    #Partial update for a customer
    if customer_id not in CustomerDB:
        raise HTTPException(status_code = 404, detail = "Customer not found")
    stored_customer = CustomerDB[customer_id].dict
    updated_customer = stored_customer | partial_customer
    CustomerDB[customer_id] = Customer(**updated_customer)
    return CustomerDB[customer_id]

@app.delete ("/api/customers/{customer_id}", status_code = 204)
def delete_customer(customer_id: int, db: Session = Depends(get_db))
    -> Response:
        user = db.get(CustomerDB, customer_id)
        if not customer:
            raise HTTPException(status_code = 404)
        db.delete(customer)
        db.commit()
        return Response(status_code = status.HTTP_204_NO_CONTENT)

#Orders
@app.post ("/api/orders", response_model = OrderRead, status_code = 201)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    customer = db.get(CustomerDB, order.owner_id)
    if not customer:
        raise HTTPException(status_code = 404, detail = "Customer ID missing")

        ord = OrderDB(
            description = order.description
            owner_id = order.owner_id
        )
        db.add(ord)
        commit_or_rollback(db, ("Order creation failed"))
        db.refresh(ord)
        return ord

@app.get ("/api/orders", response_model = list[OrderRead])
def list_orders(db: Session = Depends(get_db)):
    stmt = select(OrderDB).order_by(OrderDB.id)
    return db.execute (stmt).scalars().all()
