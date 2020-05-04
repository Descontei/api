"""
API's main module!
"""
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

# pylint: disable=invalid-name
app = FastAPI(debug=True)


def get_db():
    """
    Returns a new session for the local db
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    """
    Root route
    """
    return "Welcome home!"


# *** REGIONS ***
@app.post("/regions/", response_model=schemas.Region)
def create_region(region: schemas.RegionCreate, db: Session = Depends(get_db)):
    """
    POST for a new region
    """
    return crud.create_region(db, region)


@app.get("/regions/{region_id}", response_model=schemas.Region)
def read_region(region_id: int, db: Session = Depends(get_db)):
    """
    List a region
    """
    return crud.get_region(db, region_id)


@app.get("/regions/", response_model=List[schemas.Region])
def list_regions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_regions(db, skip, limit)


# *** CATEGORIES ***
@app.get("/categories/", response_model=List[schemas.Category])
def list_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_categories(db, skip, limit)


@app.get("/categories/{category_id}", response_model=schemas.Category)
def read_region(category_id: int, db: Session = Depends(get_db)):
    """
    List a category
    """
    return crud.get_category(db, category_id)


@app.post("/categories/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    """
    Creates a new category from a valid pydantic schema input
    """
    return crud.create_category(db=db, category=category)


# *** STORES ***
@app.get("/stores/", response_model=List[schemas.Store])
def list_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_stores(db, skip, limit)


@app.get("/stores/{store_id}", response_model=schemas.Store)
def read_product(store_id: int, db: Session = Depends(get_db)):
    return crud.get_store(db, store_id)


@app.post("/stores/", response_model=schemas.Store)
def create_category(store: schemas.StoreCreate, db: Session = Depends(get_db)):
    """
    Creates a new category from a valid pydantic schema input
    """
    return crud.create_store(db=db, store=store)


# *** PRODUCTS ***


@app.get("/products/", response_model=List[schemas.Product])
def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_products(db, skip, limit)


@app.get("/products/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    return crud.get_product(db, product_id)


@app.post("/products/", response_model=schemas.Product)
def create_category(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db=db, product=product)


# *** USERS ***
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Creates a new user from a valid pydantic schema input
    """
    db_user = crud.get_user_by_mobile(db, mobile=user.mobile)

    if db_user:
        raise HTTPException(status_code=400, detail="Mobile number already registered")

    return crud.create_user(db=db, user=user)


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user(db, user_id)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Lists all the registered users
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users
