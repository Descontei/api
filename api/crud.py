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


def create_region(db: Session, region: schemas.RegionCreate):
    """
    creates a new region from a valid pydantic schema
    """
    db_region = models.Region(**region.dict())
    db.add(db_region)
    db.commit()

    db.refresh(db_region)

    return db_region


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


def get_store(db: Session, store_id: int):
    return db.query(models.Store).filter(models.Store.id == store_id).first()


def get_stores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Store).offset(skip).limit(limit).all()


def create_store(db: Session, store: schemas.StoreCreate):
    db_store = models.Store(**store.dict())
    db.add(db_store)
    db.commit()
    db.refresh(db_store)

    return db_store


def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()


def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    return db_product

# *** ORDER
def create_order(db: Session, order: schemas.OrderCreate):
    order_data = order.dict()
    product_ids = order_data.pop("products")

    db_order = models.Order(**order_data)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    #for product_id in product_ids:
    #    pass
        # product = get_product(db, product_id)
        # db_order.products.append(product)

    # db.add(db_order)
    # db.commit()
    # db.refresh(db_order)

    return db_order


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
