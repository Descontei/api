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
