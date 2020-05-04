"""
Basic CRUD operations
"""

from sqlalchemy.orm import Session
from . import models, schemas


def get_region(db: Session, region_id: int):
    """
    Searches for an specific region by ID
    """
    return db.query(models.Region).filter(models.Region.id == region_id).first()


def get_regions(db: Session, skip: int = 0, limit: int = 100):
    """
    Lists all regions
    """
    return db.query(models.Region).offset(skip).limit(limit).all()


def get_category(db: Session, category_id: int):
    """
    Searches for an specific category by ID
    """
    return db.query(models.Category).filter(models.Category.id == category_id).first()


def get_categories(db: Session, skip: int = 0, limit: int = 100):
    """
    Lists all categories
    """
    return db.query(models.Category).offset(skip).limit(limit).all()


def create_category(db: Session, category: schemas.CategoryCreate):
    """
    creates a new category
    """
    db_category = models.Category(**category.dict())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)

    return db_category


def get_user(db: Session, user_id: int):
    """
    Searches for an specific user by ID
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_mobile(db: Session, mobile: int):
    """
    Searches for an user by its mobile phone number
    """
    return db.query(models.User).filter(models.User.mobile == mobile).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    """
    Lists all users
    """
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    """
    Creates a new user
    """
    db_user = models.User(name=user.name, mobile=user.mobile)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
