from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.database import get_db
from uuid import uuid4
from app import schemas, models
from typing import Annotated


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_product(product: schemas.ProductCreate, db:Annotated[Session, Depends(get_db)]):
    new_product = models.Product(
        product_id = f"P-{uuid4().hex}", 
        product_name = product.product_name,
        product_price = product.product_price,
        product_quantity = product.product_quantity
    )
    db.add(new_product)
    db.flush()
    new_product.product_id=(f"P-{new_product.id:03d}")
    db.commit()
    db.refresh(new_product)
    return new_product

@router.get("/api/products")
def get_products(db:Annotated[Session,Depends(get_db)],
                 status:schemas.Status| None = None,
                 q: Annotated[str| None, Query(max_length=10)] = None):
    query = db.query(models.Product)
    if status:
        query = query.filter(
            models.Product.status == status.value.capitalize()
        )
    if q:
        query = query.filter(
            models.Product.product_name.contains(q),
            models.Product.product_id.contains(q)
        )
    products = query.all()
    return products

@router.get("/{product_id}")
def get_product(product_id:str , db :Annotated[Session, Depends(get_db)]) -> schemas.ProductResponse:
    product = db.query(models.Product).filter(models.Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

@router.put("/{product_id}")
def update_product(product_id:str, product_update:schemas.ProductUpdate, db:Annotated[Session, Depends(get_db)]):
    product = db.query(models.Product).filter(models.Product.product_id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    product.status = product_update.status.value.capitalize()