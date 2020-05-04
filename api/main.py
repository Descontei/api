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


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Creates a new user from a valid pydantic schema input
    """
    db_user = crud.get_user_by_mobile(db, mobile=user.mobile)

    if db_user:
        raise HTTPException(status_code=400, detail="Mobile number already registered")

    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Lists all the registered users
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users
