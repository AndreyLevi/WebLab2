# Pydantic модели для валидации данных
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# ===== Модели для ссылок =====
class LinkCreate(BaseModel):
    url: str
    title: str
    description: Optional[str] = None

class LinkUpdate(BaseModel):
    url: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None

class Link(BaseModel):
    id: int
    url: str
    title: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True  # Для работы с ORM

# ===== Модели для пользователей =====
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool = True
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"