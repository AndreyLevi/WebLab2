from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.infrastructure.database import get_db
from app.application.service import LinkService, AuthService
from app.domain.models import LinkCreate, LinkUpdate, UserCreate, UserLogin, Token, Link
from app.application.auth import get_current_user

links_router = APIRouter(prefix="/api/links", tags=["Ссылки"])

@links_router.get("/", response_model=List[Link])
async def get_all_links(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    service = LinkService(db)
    return service.get_all(user_id=current_user["user_id"])

@links_router.get("/{link_id}", response_model=Link)
async def get_link(link_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    service = LinkService(db)
    return service.get_by_id(link_id, user_id=current_user["user_id"])

@links_router.post("/", status_code=201, response_model=Link)
async def create_link(link: LinkCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    service = LinkService(db)
    return service.create(link, user_id=current_user["user_id"])

@links_router.put("/{link_id}", response_model=Link)
async def update_link(link_id: int, link: LinkUpdate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    service = LinkService(db)
    return service.update(link_id, link, user_id=current_user["user_id"])

@links_router.delete("/{link_id}", status_code=204)
async def delete_link(link_id: int, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    service = LinkService(db)
    return service.delete(link_id, user_id=current_user["user_id"])

auth_router = APIRouter(prefix="/api/auth", tags=["Аутентификация"])

@auth_router.post("/register", response_model=dict)
async def register(user: UserCreate, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.register(user)

@auth_router.post("/login", response_model=Token)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    service = AuthService(db)
    return service.login(user.username, user.password)

@auth_router.get("/me", response_model=dict)
async def get_me(current_user: dict = Depends(get_current_user)):
    return current_user