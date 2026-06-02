from sqlalchemy import Integer, String, DateTime, Column, ForeignKey
from enum import Enum
from datetime import datetime
from app.database import Base
from sqlalchemy.orm import relationship 
from zoneinfo import ZoneInfo

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, nullable= False)
    product_id = Column(String, unique=True, nullable=False)
    product_name = Column(String, nullable= False)
    product_price = Column(Integer, nullable=False)
    product_quantity = Column(Integer, nullable=False)
    order_items = relationship('OrderItem',back_populates='product')


class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, nullable=False)
    customer_name = Column(String, nullable=False)
    customer_email = Column(String, unique=True,   nullable=False)
    phone_number = Column(String,nullable=False)
    orders = relationship('Order', back_populates='customer')
  
class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True, nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    order_date = Column(DateTime, default=lambda : datetime.now(ZoneInfo("Asia/Kolkata")))
    total_amount = Column(Integer)
    customer = relationship('Customer', back_populates='orders')
    order_items = relationship('OrderItem',back_populates='order')
    status=Column(Enum("Pending", "Cancelled", "Completed"), default="Open")

class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True, nullable=False)
    order_id = Column(Integer, ForeignKey('orders.id'),nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer)
    unit_price = Column(Integer)
    order = relationship('Order',back_populates='order_items')
    product = relationship('Product',back_populates='order_items')