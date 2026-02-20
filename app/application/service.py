# Бизнес-логика приложения
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi import HTTPException, status
from app.infrastructure.models import LinkDB
from app.infrastructure.repositories import LinkRepository, UserRepository
from app.domain.models import LinkCreate, LinkUpdate, UserCreate
from app.application.auth import get_password_hash, create_access_token, timedelta
from datetime import datetime

class LinkService:
    """Сервис для работы со ссылками"""
    
    def __init__(self, db: Session):
        self.db = db
        self.repository = LinkRepository(db)
    
    def get_all(self, user_id: int = None) -> List[LinkDB]:
        """Получить все ссылки"""
        return self.repository.get_all(user_id)
    
    def get_by_id(self, link_id: int, user_id: int = None) -> LinkDB:
        """Получить ссылку по ID"""
        link = self.repository.get_by_id(link_id, user_id)
        if not link:
            raise HTTPException(status_code=404, detail="Ссылка не найдена")
        return link
    
    def create(self,  LinkCreate, user_id: int) -> LinkDB:
        """Создать новую ссылку"""
        # Проверяем лимит (50 ссылок на пользователя)
        count = self.repository.count(user_id)
        if count >= 50:
            raise HTTPException(
                status_code=400, 
                detail="Достигнут лимит хранилища (50 записей)"
            )
        
        link = LinkDB(
            url=data.url,
            title=data.title,
            description=data.description
        )
        return self.repository.create(link, user_id)
    
    def update(self, link_id: int,  LinkUpdate, user_id: int) -> LinkDB:
        """Обновить ссылку"""
        update_data = data.dict(exclude_unset=True)
        link = self.repository.update(link_id, update_data, user_id)
        
        if not link:
            raise HTTPException(status_code=404, detail="Ссылка не найдена")
        return link
    
    def delete(self, link_id: int, user_id: int) -> dict:
        """Удалить ссылку"""
        success = self.repository.delete(link_id, user_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Ссылка не найдена")
        return {"message": "Ссылка успешно удалена"}


class AuthService:
    """Сервис для аутентификации"""
    
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)
    
    def register(self,  UserCreate) -> dict:
        """Зарегистрировать нового пользователя"""
        # Проверяем, существует ли пользователь
        if self.user_repository.get_by_username(data.username):
            raise HTTPException(
                status_code=400, 
                detail="Пользователь с таким именем уже существует"
            )
        
        if self.user_repository.get_by_email(data.email):
            raise HTTPException(
                status_code=400, 
                detail="Email уже зарегистрирован"
            )
        
        # Создаём пользователя
        user = UserDB(
            username=data.username,
            email=data.email,
            hashed_password=get_password_hash(data.password)
        )
        self.user_repository.create(user)
        
        return {"message": "Пользователь успешно зарегистрирован"}
    
    def login(self, username: str, password: str) -> dict:
        """Войти в систему и получить токен"""
        user = self.user_repository.get_by_username(username)
        
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Неверное имя пользователя или пароль",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Создаём токен
        access_token = create_access_token(
            data={"sub": user.username, "user_id": user.id}
        )
        
        return {"access_token": access_token, "token_type": "bearer"}