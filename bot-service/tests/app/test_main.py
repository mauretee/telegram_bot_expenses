import pytest
from fastapi.testclient import TestClient
from decimal import Decimal
from app.main import app, get_category_from_messages
from app.exceptions import NotExpensesFound
from app.models import User
from ..conftest import db

client = TestClient(app)

def test_get_category_from_messages_success():
    message = "I bought a sandwich for $10.00"
    category, price, description = get_category_from_messages(message)
    assert category == "Food"
    assert price == Decimal("10.00")
    assert description == "I bought a sandwich."

def test_get_category_from_messages_failure():
    message = "The cat is under the table"
    with pytest.raises(NotExpensesFound):
        category, price, description = get_category_from_messages(message)

def test_create_expesenses_not_user_found(client, user):
    response = client.post("/", json={
        "telegram_id": "2",
        "message": "I bought a sandwich for $10.00"
    })
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_create_expenses(client, user):
    response = client.post("/", json={
        "telegram_id": "1",
        "message": "I bought a sandwich for $10.00"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["category"] == "Food"
    assert data["amount"] == "10.00"
    assert data["description"] == "I bought a sandwich."

def test_create_not_an_expenses(client, user):
    response = client.post("/", json={
        "telegram_id": "1",
        "message": "The cat is under the table"
    })
    assert response.status_code == 400
    assert response.json() == {"detail": "Not an expense"}


def test_create_user(client, db):
    response = client.post("/user/", json={"telegram_id": "1"})
    assert response.status_code == 201
    users = db.query(User).filter(User.telegram_id == 1)
    user = users.first()
    assert user.telegram_id == 1

def test_create_user_already_exist(client, db, user):
    response = client.post("/user/", json={"telegram_id": "1"})
    assert response.status_code == 400
