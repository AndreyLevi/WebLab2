# Подключение к базе данных PostgreSQL
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# URL подключения к БД
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres123@localhost:5432/links_db")

# Создаём движок подключения
engine = create_engine(DATABASE_URL)

# Сессия для работы с БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для ORM моделей
Base = declarative_base()

# Dependency для получения сессии БД
def get_db():
    """
    Создаёт сессию БД и закрывает её после использования.
    Используется для Dependency Injection.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()