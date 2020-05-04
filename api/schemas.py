"""
Provides Pydantic models for the SQLAlchemy models defined in `models`
"""
from typing import List

# pylint: disable=E0611
from pydantic import BaseModel

# pylint: disable=too-few-public-methods,missing-docstring

# **** Region Classes
class RegionBase(BaseModel):
    name: str


class RegionCreate(RegionBase):
    pass


class Region(RegionBase):
    id: int
    stores: List["Store"] = []

    class Config:
        orm_mode = True


# **** Category Classes
class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int
    stores: List["Store"] = []

    class Config:
        orm_mode = True


# **** Store Classes
class StoreBase(BaseModel):
    name: str
    region_id: int
    category_id: int


class StoreCreate(StoreBase):
    pass


class Store(StoreBase):
    id: int
    products: List["Product"] = []
    orders: List["Orders"] = []

    class Config:
        orm_mode = True


# **** Product Classes
class ProductBase(BaseModel):
    name: str
    price: float


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    seller: Store

    class Config:
        orm_mode = True


# **** Order Classes
class OrderBase(BaseModel):
    store_id: int
    user_id: int


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: int
    products: List[Product] = []
    user: "User"
    store: Store

    class Config:
        orm_mode = True


# **** User Models
class UserBase(BaseModel):
    name: str
    mobile: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    stores: List[Store]
    orders: List[Order]
