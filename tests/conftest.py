import sys
from pathlib import Path

# Добавляем корень проекта в sys.path, чтобы `from app import app` работал
# и локально, и на GitHub Actions (там pytest не видит корень автоматически).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import os

import pytest

# ВАЖНО: TESTING должен быть выставлен ДО импорта app.
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