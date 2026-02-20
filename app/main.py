# Главный файл - запускает всё приложение
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.presentation.api import router

# Создаём приложение
app = FastAPI(
    title="=Веб-технологии",
    description="CRUD сервис для управления ссылками",
    version="1.0"
)

# Подключаем наш API роутер
app.include_router(router)

# Подключаем папку со статическими файлами (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="app/presentation/static"), name="static")

# Главная страница
@app.get("/")
async def root():
    return {"message": "Добро пожаловать! Откройте /static/index.html"}