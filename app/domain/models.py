# Модели данных - описываем, как выглядит наша ссылка
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4

# Модель для создания новой ссылки
class LinkCreate(BaseModel):
    url: str           # URL адрес
    title: str         # Заголовок
    description: Optional[str] = None  # Описание (не обязательно)

# Модель для обновления ссылки
class LinkUpdate(BaseModel):
    url: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None

# Модель полной ссылки (с ID)
class Link(BaseModel):
    id: str
    url: str
    title: str
    description: Optional[str] = None
    
    # Создаём новую ссылку с автоматическим ID
    @staticmethod
    def create(data: LinkCreate):
        return Link(
            id=str(uuid4()),  # Генерируем уникальный ID
            url=data.url,
            title=data.title,
            description=data.description
        )