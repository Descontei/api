"""
Provides simple functional tests for the main API
very very bad test design but keep in mind this is HACKATHON CODE
"""
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.database import Base
from api.main import app, get_db

# pylint: disable=missing-docstring, invalid-name

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.drop_all(engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    """
    Creates a test database
    """
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_create_category():
    payload = {"name": "pãodaria"}
    response = client.post("/categories/", json=payload)
    assert response.status_code == 200


def test_regions():
    payload = {"name": "brás"}

    response = client.post("/regions/", json=payload)
    assert response.status_code == 200

    response = client.get("/regions/1")
    assert response.status_code == 200

    response = client.get("/regions/")
    assert response.status_code == 200
    assert len(response.json()) == 1
