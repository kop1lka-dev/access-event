# Описание API AccessEvent

Базовый URL: `http://localhost:5000`.
Формат данных — JSON.
Авторизация — JWT в заголовке `Authorization: Bearer <token>`.

## Эндпоинты

| Метод | URL                        | Доступ            | Вход (JSON)                                                                                        | Ответы                                                  |
|-------|----------------------------|-------------------|----------------------------------------------------------------------------------------------------|---------------------------------------------------------|
| POST  | `/api/register`            | все               | `username`, `email`, `password`, `role`                                                            | 201 `user_id`; 400 ошибки валидации                     |
| POST  | `/api/login`               | все               | `email`, `password`                                                                                | 200 `token`, `role`, `user_id`; 401 неверные данные     |
| GET   | `/api/events`              | все               | —                                                                                                  | 200 список; поддержка `?inclusive=1`                    |
| GET   | `/api/events/<id>`         | все               | —                                                                                                  | 200 мероприятие; 404 нет                                |
| POST  | `/api/events`              | organizer, admin  | `title`, `event_date`, `is_inclusive`, `sign_language`, `visual_alerts`, `description`, `location` | 201 `id`; 400 ошибки; 401/403 без токена                |
| PUT   | `/api/events/<id>`         | организатор       | любые поля мероприятия                                                                             | 200 обновлённое; 403 чужое; 404 нет                     |
| DELETE| `/api/events/<id>`         | организатор       | —                                                                                                  | 200 удалено; 403 чужое; 404 нет                         |
| POST  | `/api/registrations`       | user, organizer   | `event_id`, `accessibility_request` (опц.)                                                         | 201 `id`, `status`; 400 дубль; 404 нет события          |
| GET   | `/api/registrations`       | user, organizer   | —                                                                                                  | 200 список своих регистраций                            |
| PUT   | `/api/registrations/<id>`  | organizer, admin  | `status` (`pending`/`confirmed`/`cancelled`)                                                       | 200 `status`; 400 неверный статус; 404 нет              |

## Примеры запросов и ответов

### POST /api/register

**Запрос:**
```json
{
  "username": "anna",
  "email": "anna@mail.ru",
  "password": "Passw0rd!",
  "role": "user"
}
```

**Ответ 201:**
```json
{
  "message": "Пользователь создан",
  "user_id": 1
}
```

**Ответ 400 (email занят):**
```json
{ "message": "Email уже занят" }
```

### POST /api/login

**Запрос:**
```json
{
  "email": "anna@mail.ru",
  "password": "Passw0rd!"
}
```

**Ответ 200:**
```json
{
  "message": "Вход выполнен",
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "role": "user",
  "user_id": 1
}
```

### POST /api/events (с токеном организатора)

**Заголовки:**
```
Authorization: Bearer <token>
Content-Type: application/json
```

**Запрос:**
```json
{
  "title": "Тихий кинопросмотр",
  "event_date": "2026-11-03 19:00:00",
  "is_inclusive": true,
  "sign_language": true,
  "visual_alerts": true
}
```

**Ответ 201:**
```json
{
  "message": "Мероприятие создано",
  "id": 5
}
```

### POST /api/registrations

**Заголовки:**
```
Authorization: Bearer <token>
```

**Запрос:**
```json
{
  "event_id": 5
}
```

**Ответ 201:**
```json
{
  "message": "Регистрация создана",
  "id": 12,
  "status": "pending"
}
```

**Ответ 400 (повтор):**
```json
{ "message": "Вы уже зарегистрированы" }
```

## Коды ответов

| Код | Значение                                              |
|-----|-------------------------------------------------------|
| 200 | OK — успешно                                          |
| 201 | Created — ресурс создан                               |
| 400 | Bad Request — ошибка валидации входных данных         |
| 401 | Unauthorized — нет токена или неверные данные         |
| 403 | Forbidden — токен есть, но роль/владелец не подходит  |
| 404 | Not Found — ресурс не существует                      |