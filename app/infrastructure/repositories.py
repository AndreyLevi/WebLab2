# Репозиторий для работы с базой данных
from sqlalchemy.orm import Session
from typing import List, Optional
from app.infrastructure.models import LinkDB, UserDB
from datetime import datetime

class LinkRepository:
    """
    Репозиторий для операций с ссылками.
    Все запросы к БД выполняются здесь (принцип Repository Pattern).
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, user_id: int = None) -> List[LinkDB]:
        """Получить все ссылки (все или конкретного пользователя)"""
        query = self.db.query(LinkDB)
        if user_id:
            query = query.filter(LinkDB.owner_id == user_id)
        return query.all()
    
    def get_by_id(self, link_id: int, user_id: int = None) -> Optional[LinkDB]:
        """Получить ссылку по ID"""
        query = self.db.query(LinkDB).filter(LinkDB.id == link_id)
        if user_id:
            query = query.filter(LinkDB.owner_id == user_id)
        return query.first()
    
    def create(self,  LinkDB, owner_id: int) -> LinkDB:
        """Создать новую ссылку"""
        link.owner_id = owner_id
        self.db.add(link)
        self.db.commit()
        self.db.refresh(link)
        return link
    
    def update(self, link_id: int,  dict, user_id: int = None) -> Optional[LinkDB]:
        """Обновить ссылку"""
        link = self.get_by_id(link_id, user_id)
        if not link:
            return None
        
        for key, value in data.items():
            if value is not None:
                setattr(link, key, value)
        
        link.updated_at = datetime.now()
        self.db.commit()
        self.db.refresh(link)
        return link
    
    def delete(self, link_id: int, user_id: int = None) -> bool:
        """Удалить ссылку"""
        link = self.get_by_id(link_id, user_id)
        if not link:
            return False
        
        self.db.delete(link)
        self.db.commit()
        return True
    
    def count(self, user_id: int = None) -> int:
        """Посчитать количество ссылок"""
        query = self.db.query(LinkDB)
        if user_id:
            query = query.filter(LinkDB.owner_id == user_id)
        return query.count()


class UserRepository:
    """Репозиторий для операций с пользователями"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_username(self, username: str) -> Optional[UserDB]:
        """Найти пользователя по имени"""
        return self.db.query(UserDB).filter(UserDB.username == username).first()
    
    def get_by_email(self, email: str) -> Optional[UserDB]:
        """Найти пользователя по email"""
        return self.db.query(UserDB).filter(UserDB.email == email).first()
    
    def get_by_id(self, user_id: int) -> Optional[UserDB]:
        """Найти пользователя по ID"""
        return self.db.query(UserDB).filter(UserDB.id == user_id).first()
    
    def create(self,  UserDB) -> UserDB:
        """Создать нового пользователя"""
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user