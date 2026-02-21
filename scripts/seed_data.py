import sys
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

# Добавляем корень проекта в путь для корректного импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.infrastructure.database import SessionLocal, engine, Base
from app.infrastructure.models import UserDB, LinkDB
from app.application.auth import hash_password

def seed_data():
    # Создаем таблицы, если их нет
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Проверяем, есть ли уже пользователь
        existing_user = db.query(UserDB).filter(UserDB.username == "testuser").first()
        if existing_user:
            print("Пользователь testuser уже существует")
            return

        user = UserDB(
            username="testuser", 
            email="test@example.com", 
            password_hash=hash_password("password123")
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"Пользователь создан: {user.username}")
        
        test_links = [
            {"url": "https://google.com", "title": "Google", "description": "Поисковик"},
            {"url": "https://github.com", "title": "GitHub", "description": "Хостинг кода"},
            {"url": "https://stackoverflow.com", "title": "StackOverflow", "description": "Вопросы и ответы"},
        ]
        for link_data in test_links:
            link = LinkDB(
                url=link_data["url"], 
                title=link_data["title"], 
                description=link_data["description"], 
                owner_id=user.id
            )
            db.add(link)
        db.commit()
        print(f"Создано {len(test_links)} тестовых ссылок")
    except Exception as e:
        db.rollback()
        print(f"Ошибка: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()