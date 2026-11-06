import logging

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from check_storage import BookStorage

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)


class BookInput(BaseModel):
    title: str
    price: float = Field(ge=0)


class BookResponse(BookInput):
    id: int


app = FastAPI(title="Books Database API")
storage = BookStorage()


@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int):
    book = storage.get_book(book_id)
    if book is None:
        logger.warning(f"Book not found: {book_id}")
        raise HTTPException(status_code=404, detail="Book not found")
    logger.info(f"Retrieved book: id={book_id}")
    return book

@app.post("/books", response_model=BookResponse)
def add_book(book: BookInput):
    id = storage.add_book(book.title, book.price)
    logger.info(f"New book ID: {id}")
    return storage.get_book(id)


@app.get("/books", response_model=list[BookResponse])
def list_books(
    min_price: float = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1)
):
    rows = storage.list_books(min_price, limit)
    logger.info(f"Returned {len(rows)} rows")
    return rows

@app.get("/search/books", response_model=list[BookResponse])
def search_books(
    min_price: float = Query(ge=0),
    max_price: float = Query(ge=0)
):
    if min_price > max_price:
        logger.warning(f"Min price cannot be greater than max price")
        raise HTTPException(status_code=400, detail="min_price cannot exceed max_price")

    rows = storage.search_books(min_price, max_price)
    logger.info(f"Returned row count: {len(rows)}")
    return rows
    
