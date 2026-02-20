    # Хранилище данных - сохраняем ссылки в памяти
from typing import List, Optional
from app.domain.models import Link

class Storage:
    def __init__(self):
        self.links = []  # Список для хранения ссылок
        self.MAX_LIMIT = 50  # Максимум 50 записей
    
    # Получить все ссылки
    def get_all(self) -> List[Link]:
        return self.links
    
    # Найти ссылку по ID
    def get_by_id(self, link_id: str) -> Optional[Link]:
        for link in self.links:
            if link.id == link_id:
                return link
        return None
    
    # Добавить новую ссылку
    def add(self, link: Link) -> bool:
        # Проверяем, не превышен ли лимит
        if len(self.links) >= self.MAX_LIMIT:
            return False
        self.links.append(link)
        return True
    
    # Обновить ссылку
    def update(self, link_id: str, data: dict) -> Optional[Link]:
        link = self.get_by_id(link_id)
        if not link:
            return None
        
        # Обновляем только те поля, которые переданы
        if data.get('url'):
            link.url = data['url']
        if data.get('title'):
            link.title = data['title']
        if data.get('description') is not None:
            link.description = data['description']
        
        return link
    
    # Удалить ссылку
    def delete(self, link_id: str) -> bool:
        link = self.get_by_id(link_id)
        if link:
            self.links.remove(link)
            return True
        return False

# Создаём общее хранилище для всего приложения
storage = Storage()