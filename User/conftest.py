from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from main import app
from model import get_db, Base

engine = create_engine(f'postgresql+psycopg2://postgres:12345@localhost:5432/Test_Book_Store')
session = Session(engine)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)


@pytest.fixture
def user_data():
    return {
        'user_name': "Omkar@123",
        "password": "Omkar@123",
        "first_name": "Omkar",
        "last_name": "Bhise",
        "email": "omkarbhise8635@gmail.com",
        "phone": 9960401728,
        "city": "Latur",
        "state": "Maharashtra",
        "super_user": "99604017",
        "is_verified": True
    }


@pytest.fixture
def user_login():
    return {
        "user_name": "Omkar@123",
        "password": "Omkar@123"
    }


@pytest.fixture
def not_super_user():
    return {
        "user_name": "Bhise@123",
        "password": "Bhise@123",
        "first_name": "Omkar",
        "last_name": "Bhise",
        "email": "omkarbhise8743@gmail.com",
        "phone": 9960401728,
        "city": "Latur",
        "state": "Maharashtra",
        "is_verified": False
    }


@pytest.fixture
def super_user_login():
    return {
        "user_name": "Bhise@123",
        "password": "Bhise@123"
    }

@pytest.fixture
def not_valid_user_data():
    return {
        "user_name": "Omkar@123",
        "password": "Omkar@123",
        "first_name": 1234,
        "last_name": "Bhise",
        "email": "omkarbhise8635@gmail.com",
        "phone": 9960401728,
        "city": "Latur",
        "state": "Maharashtra"
    }

@pytest.fixture
def login_error():
    return {
        'user_name':"Omkar@123",
        "password":"Omkar"
    }