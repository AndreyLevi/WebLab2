# Бизнес-логика - правила работы с ссылками
from app.infrastructure.storage import storage
from app.domain.models import Link, LinkCreate, LinkUpdate
from fastapi import HTTPException

class LinkService:
    
    # Получить все ссылки
    def get_all(self):
        return storage.get_all()
    
    # Получить одну ссылку по ID
    def get_one(self, link_id: str):
        link = storage.get_by_id(link_id)
        if not link:
            # Если не нашли - возвращаем ошибку 404
            raise HTTPException(status_code=404, detail="Ссылка не найдена")
        return link
    
    # Создать новую ссылку
    def create(self, data: LinkCreate):
        link = Link.create(data)  # Создаём объект ссылки
        success = storage.add(link)  # Сохраняем в хранилище
        
        if not success:
            # Если хранилище переполнено
            raise HTTPException(
                status_code=400, 
                detail="Достигнут лимит хранилища (50 записей)"
            )
        return {"message": "Ссылка успешно создана"}
    
    # Обновить ссылку
    def update(self, link_id: str, data: LinkUpdate):
        # Преобразуем данные в словарь, убираем пустые значения
        update_data = data.dict(exclude_unset=True)
        link = storage.update(link_id, update_data)
        
        if not link:
            raise HTTPException(status_code=404, detail="Ссылка не найдена")
        return {"message": "Ссылка успешно обновлена"}
    
    # Удалить ссылку
    def delete(self, link_id: str):
        success = storage.delete(link_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Ссылка не найдена")
        return {"message": "Ссылка успешно удалена"}

# Создаём сервис для использования
link_service = LinkService()