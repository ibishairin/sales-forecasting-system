from pydantic import BaseModel
from datetime import datetime
from enum import Enum
from typing import Optional

class UserRegister(BaseModel):
    phone_number : str
    customer_name: str
    customer_email: str
    password : str

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    password : str

class ProductCreate(BaseModel):
    product_name : str
    product_price : int
    product_quantity : int

class ProductResponse(ProductCreate):
    id : int
    product_id : str

    class Config:
        orm_mode = True

class OrderCreate(BaseModel):
    customer_id : int
    order_date : datetime
    total_amount : int

class OrderResponse(OrderCreate):
    id : int

    class Config:
        orm_mode = True

class OrderItemCreate(BaseModel):
    order_id : int
    product_id :int
    quantity : int


class OrderItemResponse(OrderItemCreate):
    id: int
    order_id: int
    product_id: int
    quantity: int
    unit_price: int

    class Config:
        orm_mode = True


class Status(str,Enum):
    PENDING = 'pending'
    CANCELLED = 'completed'
    COMPLETED = 'cancelled'

