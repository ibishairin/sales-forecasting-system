from fastapi import APIRouter, Depends, HTTPException, status, Query, Response, List
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.database import get_db
from app import schemas, models
from typing import Annotated


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get("/", response_class=List[schemas.ProductResponse])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ProductResponse)

def create_product(product:schemas.ProductCreate, db : Session = Depends(get_db)):
    new_product = models.Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product



@router.get("/{id}", response_class=schemas.ProductResponse)
def get_products(product:schemas.ProductResponse, db : Session = Depends(get_db)):
    products = db.query(models.Product).first()
    return products



def get_prodcut(id:int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id ).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

    

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id:int,db:Session= Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == id )
    if product.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    product.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def update_product(id:int, update_product: schemas.ProductResponse, db:Session= Depends(get_db)):
    product_query = db.query(models.Product).filter(models.Product.id == id )
    product= product_query.first()
    if product == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "Product not found")
    product_query.update(update_product.dict(), synchronize_session=False)
    db.commit()
    return product_query.first()

