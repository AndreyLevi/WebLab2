# Точка входа в приложение
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.presentation.api import links_router, auth_router
from app.infrastructure.database import engine, Base

# Создаём таблицы в БД (если не существуют)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Лабораторная работа №2",
    description="Веб-приложение с ORM, PostgreSQL, Docker и аутентификацией",
    version="2.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(links_router)
app.include_router(auth_router)

# Статические файлы
app.mount("/static", StaticFiles(directory="app/presentation/static"), name="static")

@app.get("/")
async def root():
    return {"message": "Откройте /static/login.html для входа"}