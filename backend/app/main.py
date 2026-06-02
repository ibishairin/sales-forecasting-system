from fastapi import FastAPI
from app.database import Base,engine
from app import models

app = FastAPI()
Base.metadata.create_all(bind = engine)

@app.get("/")
def root():
    return {"message": "Hello World ! "}

@app.post("/api/products")
def create_product(product)