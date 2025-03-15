from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse, HTMLResponse
from models.book import Book
from services.book_service import BookService
import zipfile
import os
import hashlib
import logging
import pandas as pd

router = APIRouter(prefix="/livros")

@router.get("/", response_model=list[Book])
def get_books(
    title: str = Query(None, description="Filtrar por título"),
    author: str = Query(None, description="Filtrar por autor"),
    year: int = Query(None, description="Filtrar por ano"),
    genre: str = Query(None, description="Filtrar por gênero"),
    skip: int = Query(0, description="Pegar a partir do registro de índice"),
    limit: int = Query(10, description="Número máximo de registros a serem retornados")
):
    books = BookService.read_books()
    if title:
        books = [book for book in books if title.lower() in book.title.lower()]
    if author:
        books = [book for book in books if author.lower() in book.author.lower()]
    if year:
        books = [book for book in books if book.year == year]
    if genre:
        books = [book for book in books if genre.lower() in book.genre.lower()]
    logging.info("Livros recuperados com filtros - título: %s, autor: %s, ano: %s, gênero: %s", title, author, year, genre)
    return books[skip:skip + limit]

@router.get("/count", response_model=int)
def get_books_count():
    df = pd.read_csv("books.csv")
    count = len(df)
    logging.info("Quantidade de livros recuperada - Total: %d", count)
    return count

@router.get("/download", response_class=FileResponse)
def download_books():
    csv_file = "books.csv"
    zip_file = "books.zip"
    
    with zipfile.ZipFile(zip_file, 'w') as zipf:
        zipf.write(csv_file, os.path.basename(csv_file))
    
    logging.info("Arquivo CSV dos livros compactado")
    return FileResponse(zip_file, media_type='application/zip', filename=zip_file)

@router.get("/hash", response_model=dict)
def get_csv_hash():
    csv_file = "books.csv"
    sha256_hash = hashlib.sha256()
    with open(csv_file, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    hash_value = sha256_hash.hexdigest()
    logging.info("Hash SHA256 do arquivo CSV: %s", hash_value)
    return {"hash_sha256": hash_value}

@router.get("/interface", response_class=HTMLResponse)
def get_interface():
    with open("static/index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

@router.get("/{book_id}", response_model=Book)
def get_book(book_id: int):
    book = BookService.get_book(book_id)
    if book:
        logging.info("Livro recuperado - ID: %d", book_id)
        return book
    logging.error("Livro não encontrado - ID: %d", book_id)
    raise HTTPException(status_code=404, detail=f"Livro com ID {book_id} não encontrado")

@router.post("/", response_model=Book)
def create_book(book: Book):
    if BookService.create_book(book):
        logging.info("Livro criado - ID: %d", book.id)
        return book
    logging.error("Falha ao criar o livro - ID: %d", book.id)
    raise HTTPException(status_code=400, detail=f"Livro com ID {book.id} já existe")

@router.put("/{book_id}", response_model=Book)
def update_book(book_id: int, updated_book: Book):
    book = BookService.update_book(book_id, updated_book)
    if book:
        logging.info("Livro atualizado - ID: %d", book_id)
        return book
    logging.error("Falha ao atualizar o livro - ID: %d", book_id)
    raise HTTPException(status_code=404, detail=f"Livro com ID {book_id} não encontrado")

@router.delete("/{book_id}", response_model=Book)
def delete_book(book_id: int):
    book = BookService.delete_book(book_id)
    if book:
        logging.info("Livro deletado - ID: %d", book_id)
        return book
    logging.error("Falha ao deletar o livro - ID: %d", book_id)
    raise HTTPException(status_code=404, detail=f"Livro com ID {book_id} não encontrado")