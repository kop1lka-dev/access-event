import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")

    # Если выставлен TESTING — используем SQLite в памяти (тесты не трогают
    # рабочую БД и не создают файлов на диске).
    # Иначе — DATABASE_URL из .env или локальный файл accessevent.db.
    if os.environ.get("TESTING"):
        SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    else:
        SQLALCHEMY_DATABASE_URI = os.environ.get(
            "DATABASE_URL", "sqlite:///accessevent.db"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_EXPIRATION_HOURS = 24