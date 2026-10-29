# TeaGuardian — защита проекта

## Цель проекта

TeaGuardian — это приложение для чайного любителя: оно позволяет сохранять рецепты заваривания, отслеживать любимые сорта чая и использовать таймер для точного времени заваривания.

## Архитектура

### Backend
- FastAPI
- SQLAlchemy
- SQLite
- JWT authentication
- Protected API routes for recipes

### Frontend
- Kivy desktop app
- Simple screen-based interface
- Login / register flow
- Recipe CRUD
- Tea timer screen

## Основные функции

- Регистрация и вход пользователя
- Генерация access/refresh token
- Защита маршрутов рецептов
- Создание, редактирование, удаление рецепта
- Поиск по названию рецепта
- Таймер заваривания по выбранному рецепту
- Инициализация базы данных и начальных сортов чая

## Используемые технологии

- Python 3.13
- FastAPI
- SQLAlchemy
- Pydantic
- Kivy
- SQLite

## Как запускать проект

1. Создать виртуальное окружение
2. Установить зависимости из `requirements.txt`
3. Запустить backend через `start_backend.bat`
4. Запустить client через `start_client.bat`
5. Открыть Swagger UI на http://127.0.0.1:8000/docs

## Проверка

Проверку можно выполнить по простой цепочке:

1. Register user
2. Login user
3. Create recipe
4. Refresh recipe list
5. Start timer
6. Confirm the timer counts down correctly

## Что важно подчеркнуть в защите

- Бэкенд и клиент разделены по слоям
- Используется JWT-авторизация
- База данных построена на SQLite и SQLAlchemy
- Основной сценарий пользователя понятен и реализован без лишнего усложнения
- Приложение легко запускается на обычном ПК

## Ключевые файлы проекта

- `server/app/main.py` — запуск API и регистрация роутеров
- `server/app/models/entities.py` — схема таблиц
- `server/app/routers/auth.py` — авторизация
- `server/app/routers/recipes.py` — CRUD рецептов
- `client/main.py` — Kivy клиент
- `client/theme.py` — цветовая палитра и базовые стили

## Итог

Проект демонстрирует полный цикл: пользовательская регистрация, безопасный доступ к данным, хранение рецептов и удобный таймер заваривания. Это соответствует условиям учебной разработки и позволяет быстро проверить приложение на локальном компьютере.
