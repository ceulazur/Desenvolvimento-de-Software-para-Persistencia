from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from routers import book_router
from services.book_service import BookService
from models.book import Book
import os
import logging

app = FastAPI()

app.include_router(book_router.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="API de Livros",
        version="1.0.0",
        description="API para gerenciamento de livros com operações CRUD",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)