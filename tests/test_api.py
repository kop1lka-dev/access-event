"""Unit-тесты API-эндпоинтов AccessEvent.

Проверяют работу Flask-маршрутов через app.test_client():
регистрация, вход, JWT, создание мероприятий, регистрация на них.

Фикстура client приходит из tests/conftest.py.
"""


# ---------- Вспомогательная функция ----------

def _register_and_login(client, email, role="user"):
    """Регистрирует пользователя и возвращает его JWT.

    Имя начинается с _ — pytest не примет её за тест.
    """
    client.post("/api/register", json={
        "username": email.split("@")[0],
        "email": email,
        "password": "Passw0rd!",
        "role": role,
    })
    resp = client.post("/api/login", json={
        "email": email,
        "password": "Passw0rd!",
    })
    return resp.get_json()["token"]


# ---------- Базовые тесты (5 из методички, адаптированные) ----------

def test_register_success(client):
    """Регистрация с валидными данными → 201 и user_id."""
    resp = client.post("/api/register", json={
        "username": "anna",
        "email": "anna@mail.ru",
        "password": "Passw0rd!",
        "role": "user",
    })
    assert resp.status_code == 201
    assert "user_id" in resp.get_json()


def test_register_invalid_email_rejected(client):
    """Email без @ → 400."""
    resp = client.post("/api/register", json={
        "username": "bob",
        "email": "not-an-email",
        "password": "Passw0rd!",
        "role": "user",
    })
    assert resp.status_code == 400


def test_login_returns_token(client):
    """Правильный логин → 200 и token."""
    client.post("/api/register", json={
        "username": "org",
        "email": "org@mail.ru",
        "password": "Passw0rd!",
        "role": "organizer",
    })
    resp = client.post("/api/login", json={
        "email": "org@mail.ru",
        "password": "Passw0rd!",
    })
    assert resp.status_code == 200
    assert "token" in resp.get_json()


def test_create_event_requires_organizer_token(client):
    """Создание мероприятия без токена → 401 или 403."""
    resp = client.post("/api/events", json={"title": "Лекция"})
    assert resp.status_code in (401, 403)


def test_events_list_public(client):
    """GET /api/events доступен без авторизации → 200."""
    resp = client.get("/api/events")
    assert resp.status_code == 200


# ---------- Три собственных теста ----------

def test_create_event_with_token(client):
    """Создание мероприятия организатором с токеном → 201 и id."""
    token = _register_and_login(client, "org3@mail.ru", role="organizer")
    headers = {"Authorization": "Bearer " + token}

    resp = client.post("/api/events", json={
        "title": "Тихий кинопросмотр",
        "event_date": "2026-11-03 19:00:00",
        "is_inclusive": True,
    }, headers=headers)

    assert resp.status_code == 201
    assert "id" in resp.get_json()


def test_register_for_event(client):
    """Участник регистрируется на созданное мероприятие → 201."""
    org_token = _register_and_login(client, "org4@mail.ru", role="organizer")
    client.post("/api/events", json={
        "title": "Экскурсия",
        "event_date": "2026-11-03 12:00:00",
    }, headers={"Authorization": "Bearer " + org_token})

    # Получаем список мероприятий — берём id первого
    events = client.get("/api/events").get_json()
    event_id = events[0]["id"]

    # Участник
    user_token = _register_and_login(client, "p3@mail.ru", role="user")
    resp = client.post(
        "/api/registrations",
        json={"event_id": event_id},
        headers={"Authorization": "Bearer " + user_token},
    )
    assert resp.status_code == 201


def test_my_registrations_list(client):
    """GET /api/registrations с токеном → 200 (пустой список)."""
    token = _register_and_login(client, "p4@mail.ru", role="user")
    headers = {"Authorization": "Bearer " + token}

    resp = client.get("/api/registrations", headers=headers)
    assert resp.status_code == 200