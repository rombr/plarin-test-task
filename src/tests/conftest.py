import os
import sys
import json

from pytest import fixture
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient


# src for test running
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)


from db import get_database  # noqa
from config import (
    MONGODB_URL, MAX_CONNECTIONS_COUNT, MIN_CONNECTIONS_COUNT,
    DB_NAME,
)  # noqa


@fixture(scope="session")
def db():
    test_db_name = f'test_{DB_NAME}'
    try:
        client = AsyncIOMotorClient(
            str(MONGODB_URL),
            maxPoolSize=MAX_CONNECTIONS_COUNT,
            minPoolSize=MIN_CONNECTIONS_COUNT
        )
        db = client[test_db_name]

        yield db
    finally:
        client.drop_database(test_db_name)
        client.close()


@fixture(scope="session")
def test_client(db):
    from main import app

    app.dependency_overrides[get_database] = db

    with TestClient(app) as test_client:
        yield test_client


@fixture(scope="function")
def employees_fixture(db):
    f_name = os.path.abspath(os.path.join(
        os.path.dirname(__file__),
        '..', '..', 'fixtures', 'employees.json')
    )
    with open(f_name) as f:
        try:
            employees = json.load(f)

            res = db.employees.insert_many(employees)

            yield res
        finally:
            db.employees.drop()
