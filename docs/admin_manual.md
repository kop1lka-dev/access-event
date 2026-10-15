# Руководство администратора AccessEvent

## 1. Системные требования

- Python 3.11+ (рекомендуется 3.13)
- SQLite 3 (по умолчанию) **или** PostgreSQL 15+ (для продакшена)
- Docker 24+ и Docker Compose (для контейнерного запуска)
- 64-разрядная ОС: Windows 10/11, macOS, Linux

## 2. Развёртывание

### 2.1. Локально (для разработки)

1. Создайте виртуальное окружение:
   ```powershell
   python -m venv venv
   venv\Scripts\Activate.ps1     # Windows
   source venv/bin/activate       # macOS/Linux