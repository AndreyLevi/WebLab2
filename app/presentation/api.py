# API эндпоинты - точки входа для запросов
from fastapi import APIRouter
from app.domain.models import LinkCreate, LinkUpdate
from app.application.service import link_service
from typing import List

# Создаём роутер для группы ссылок
router = APIRouter(prefix="/api/links", tags=["Ссылки"])

# GET - получить все ссылки
@router.get("/")
async def get_all_links() -> List:
    """Вернуть список всех ссылок"""
    return link_service.get_all()

# GET - получить одну ссылку
@router.get("/{link_id}")
async def get_link(link_id: str):
    """Вернуть ссылку по ID"""
    return link_service.get_one(link_id)

# POST - создать новую ссылку
@router.post("/")
async def create_link(link: LinkCreate):
    """Создать новую ссылку"""
    return link_service.create(link)

# PUT - обновить ссылку
@router.put("/{link_id}")
async def update_link(link_id: str, link: LinkUpdate):
    """Обновить существующую ссылку"""
    return link_service.update(link_id, link)

# DELETE - удалить ссылку
@router.delete("/{link_id}")
async def delete_link(link_id: str):
    """Удалить ссылку по ID"""
    return link_service.delete(link_id)