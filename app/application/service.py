from sqlalchemy.orm import Session
from typing import List
from fastapi import HTTPException, status
from app.infrastructure.repositories import LinkRepository, UserRepository
from app.domain.models import LinkCreate, LinkUpdate, UserCreate
from app.application.auth import create_access_token, hash_password, verify_password

class LinkService:
    def __init__(self, db: Session):
        self.repository = LinkRepository(db)
    
    def get_all(self, user_id: int) -> List:
        return self.repository.get_all(user_id)
    
    def get_by_id(self, link_id: int, user_id: int):
        link = self.repository.get_by_id(link_id, user_id)
        if not link:
            raise HTTPException(status_code=404, detail="Ссылка не найдена")
        return link
    
    def create(self, data: LinkCreate, user_id: int):
        count = self.repository.count(user_id)
        if count >= 50:
            raise HTTPException(status_code=400, detail="Достигнут лимит хранилища (50 записей)")
        
        link_data = {
            "url": data.url,
            "title": data.title,
            "description": data.description
        }
        return self.repository.create(link_data, user_id)
    
    def update(self, link_id: int, data: LinkUpdate, user_id: int):
        update_data = data.dict(exclude_unset=True)
        link = self.repository.update(link_id, user_id, update_data)
        if not link:
            raise HTTPException(status_code=404, detail="Ссылка не найдена")
        return link
    
    def delete(self, link_id: int, user_id: int) -> dict:
        success = self.repository.delete(link_id, user_id)
        if not success:
            raise HTTPException(status_code=404, detail="Ссылка не найдена")
        return {"message": "Ссылка успешно удалена"}

class AuthService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
    
    def register(self, data: UserCreate) -> dict:
        if self.repository.get_by_username(data.username):
            raise HTTPException(status_code=400, detail="Пользователь существует")
        if self.repository.get_by_email(data.email):
            raise HTTPException(status_code=400, detail="Email занят")
        
        user_data = {
            "username": data.username,
            "email": data.email,
            "password_hash": hash_password(data.password)
        }
        self.repository.create(user_data)
        return {"message": "Пользователь зарегистрирован"}
    
    def login(self, username: str, password: str) -> dict:
        user = self.repository.get_by_username(username)
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Неверный логин или пароль")
        
        access_token = create_access_token(data={"sub": user.username, "user_id": user.id})
        return {"access_token": access_token, "token_type": "bearer"}