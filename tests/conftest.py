import os

import pytest

# ВАЖНО: эта строка должна быть ДО импорта app.
# config.py читает TESTING в момент создания app и выбирает SQLite вместо PostgreSQL.
os.environ.setdefault("TESTING", "1")

from app import app, db


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        with app.app_context():
            db.create_all()
            yield c
            db.session.remove()
            db.drop_all()