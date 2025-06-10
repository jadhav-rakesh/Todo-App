from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..database import Base
from ..main import app
from ..models import Todos, Users
from fastapi.testclient import TestClient
import pytest
from ..routers.auth import bcrypt_context

SQLALCHEMY_DATABASE_URL_TEST = "sqlite:///./testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL_TEST,
    connect_args={"check_same_thread": False},
    poolclass= StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db 
    finally:
        db.close()

def override_get_current_user():
    return {"username": "rakeshtest", "id": 1, "user_role": "admin"}

client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(
        title = "Learn to code!",
        description = "Need to learn everday!",
        priority=5,
        complete=False,
        owner_id=1
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


@pytest.fixture
def test_user():
    user = Users(
        username="rakeshtest",
        email="rakesh@gmail.com",
        first_name="Rakesh",
        last_name="J",
        hashed_password=bcrypt_context.hash("rakeshjadhav"),
        role="admin",
        phone_number="(91)-12345-6789"
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user 
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()