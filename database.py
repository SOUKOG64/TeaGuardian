import os
from sqlalchemy import create_engine, Column, Integer, String, Boolean, inspect, text
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
SessionLocal = None

# Модель рецепта (дневник завариваний)
class Recipe(Base):
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tea_name = Column(String, nullable=False)
    temperature = Column(Integer, nullable=False)
    brew_time = Column(Integer, nullable=False) # Время в секундах
    notes = Column(String, default="")
    is_default = Column(Boolean, nullable=False, default=False, server_default=text("0"))


DEFAULT_RECIPES = [
    {"tea_name": "Да Хун Пао (武夷岩茶)", "temperature": 93, "brew_time": 6},
    {"tea_name": "Те Гуаньинь (铁观音)", "temperature": 80, "brew_time": 6},
    {"tea_name": "Шен Пуэр (生普洱)", "temperature": 80, "brew_time": 9},
    {"tea_name": "Шу Пуэр (熟普洱)", "temperature": 93, "brew_time": 9},
    {"tea_name": "Жёлтый чай (君山银针)", "temperature": 73, "brew_time": 4},
]

def init_db(data_dir):
    """Инициализация БД по пути, безопасному для Android"""
    global SessionLocal
    
    # Формируем абсолютный путь к файлу БД
    os.makedirs(data_dir, exist_ok=True)
    db_path = os.path.join(data_dir, 'teaguardian.db')
    
    # Подключаемся к SQLite
    engine = create_engine(f'sqlite:///{db_path}')
    
    # Создаем таблицы, если их нет
    Base.metadata.create_all(engine)

    # create_all не обновляет таблицы, созданные предыдущими версиями приложения.
    columns = {column["name"] for column in inspect(engine).get_columns(Recipe.__tablename__)}
    if "is_default" not in columns:
        with engine.begin() as connection:
            connection.execute(text(
                "ALTER TABLE recipes ADD COLUMN is_default BOOLEAN NOT NULL DEFAULT 0"
            ))
    
    # Создаем фабрику сессий
    SessionLocal = sessionmaker(bind=engine)

def add_recipe(tea_name, temperature, brew_time, notes=""):
    """API: Добавление нового рецепта в базу"""
    if SessionLocal is None:
        raise RuntimeError("База данных не инициализирована!")
        
    session = SessionLocal()
    try:
        new_recipe = Recipe(
            tea_name=tea_name,
            temperature=temperature,
            brew_time=brew_time,
            notes=notes,
            is_default=False,
        )
        session.add(new_recipe)
        session.commit()
    finally:
        session.close()

def load_default_recipes():
    """Добавляет стандартные рецепты, не создавая дубликаты при повторном запуске."""
    if SessionLocal is None:
        raise RuntimeError("База данных не инициализирована!")

    session = SessionLocal()
    try:
        existing_names = {
            name for (name,) in session.query(Recipe.tea_name)
            .filter(Recipe.is_default.is_(True))
            .all()
        }
        for recipe in DEFAULT_RECIPES:
            if recipe["tea_name"] not in existing_names:
                session.add(Recipe(**recipe, is_default=True))
        session.commit()
    finally:
        session.close()

def get_all_recipes():
    """API: Получение всех рецептов в виде списка словарей"""
    if SessionLocal is None:
        raise RuntimeError("База данных не инициализирована!")
        
    session = SessionLocal()
    try:
        recipes = session.query(Recipe).all()
        return [
            {
                "id": recipe.id,
                "tea_name": recipe.tea_name,
                "temp": recipe.temperature,
                "time": recipe.brew_time,
                "notes": recipe.notes,
                "is_default": recipe.is_default,
            }
            for recipe in recipes
        ]
    finally:
        session.close()

def get_default_recipes():
    """API: Получение стандартных рецептов для выбора в интерфейсе."""
    if SessionLocal is None:
        raise RuntimeError("База данных не инициализирована!")

    session = SessionLocal()
    try:
        recipes = session.query(Recipe).filter(Recipe.is_default.is_(True)).all()
        return [
            {
                "id": recipe.id,
                "tea_name": recipe.tea_name,
                "temp": recipe.temperature,
                "time": recipe.brew_time,
                "notes": recipe.notes,
                "is_default": recipe.is_default,
            }
            for recipe in recipes
        ]
    finally:
        session.close()

def get_diary_recipes():
    """API: Получение пользовательских записей без встроенных рецептов."""
    if SessionLocal is None:
        raise RuntimeError("База данных не инициализирована!")

    session = SessionLocal()
    try:
        recipes = session.query(Recipe).filter(Recipe.is_default.is_(False)).all()
        return [
            {
                "id": recipe.id,
                "tea_name": recipe.tea_name,
                "temp": recipe.temperature,
                "time": recipe.brew_time,
                "notes": recipe.notes,
                "is_default": recipe.is_default,
            }
            for recipe in recipes
        ]
    finally:
        session.close()