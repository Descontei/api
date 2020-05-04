"""
Defines SQLAlchemy Models for the whole API
"""
from sqlalchemy import Column, ForeignKey, Integer, String, Float, Table
from sqlalchemy.orm import relationship

from .database import Base

# pylint: disable=too-few-public-methods,invalid-name,missing-docstring


class Region(Base):
    """
    A region is a geographic area that holds the stores. This is the
    main geo-reference used in the moment.
    """

    __tablename__ = "regions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    stores = relationship("Store", back_populates="region")


class Category(Base):
    """
    Categories that a store appears into
    """

    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    stores = relationship("Store", back_populates="category")


class Store(Base):
    """
    Model that defines a Store that's able to sell goods
    """

    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    region_id = Column(Integer, ForeignKey("regions"))
    category_id = Column(Integer, ForeignKey("categories.id"))

    region = relationship("Region", back_populates="stores")
    category = relationship("Category", back_populates="stores")
    products = relationship("Product", back_populates="seller")
    orders = relationship("Order", back_populates="store")


class Product(Base):
    """
    Model for the sellable products in the stores
    """

    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float)
    seller_id = Column(Integer, ForeignKey("stores.id"))
    seller = relationship("Store", back_populates="products")


order_products = Table(
    "order_products",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("products.id")),
    Column("order_id", Integer, ForeignKey("orders.id")),
)


class Order(Base):
    id = Column(Integer, primary_key=True, index=True)
    store_id = Column(Integer, ForeignKey("stores.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    products = relationship("Product", secondary=order_products)

    user = relationship("User", back_populates="orders")
    store = relationship("Store", back_populates="orders")


user_stores = Table(
    "user_stores",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("store_id", Integer, ForeignKey("store.id")),
)


class User(Base):
    """
    Model for the user table
    """

    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    mobile = Column(String, index=True)

    stores = relationship("Store", secondary=user_stores)
    orders = relationship("Order", back_populates="user")
