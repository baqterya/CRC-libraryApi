import uvicorn
from fastapi import FastAPI, Depends

from app.database import engine, get_db
import app.schema as schema
import app.models as models
import app.crud_utils as crud_utils

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    return {"message": "Welcome to the libraryAPI", "explore": "/docs"}


@app.get("/api/v1/author/{author_id}", response_model=schema.AuthorBase)
def get_author_by_id(author_id: int, db=Depends(get_db)):
    db_response = crud_utils.get_author_by_id(db, author_id)
    if db_response.db_object is None:
        raise db_response.exception
    return db_response.db_object


@app.get("/api/v1/author/{name_last}/{name_first}", response_model=schema.AuthorBase)
def get_author_by_name(name_first: str, name_last: str, db=Depends(get_db)):
    db_response = crud_utils.get_author_by_name(db, name_first, name_last)
    if db_response.db_object is None:
        raise db_response.exception
    return db_response.db_object


@app.get("/api/v1/author/", response_model=list[schema.AuthorBase])
def get_authors(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    return crud_utils.get_authors(db, skip, limit)


@app.post("/api/v1/author/", response_model=schema.AuthorCreate)
def create_author(author: schema.AuthorCreate, db=Depends(get_db)):
    db_response = crud_utils.create_author(db, author)
    if db_response.db_object is None:
        raise db_response.exception
    return db_response.db_object


@app.put("/api/v1/author/{author_id}", response_model=schema.AuthorBase)
def update_author(author_id: int, author: schema.AuthorUpdate, db=Depends(get_db)):
    db_response = crud_utils.update_author(db, author_id, author)
    if db_response.db_object is None:
        raise db_response.exception
    return db_response.db_object


@app.delete("/api/v1/author/{author_id}", response_model=schema.AuthorBase)
def delete_author(author_id: int, db=Depends(get_db)):
    db_response = crud_utils.delete_author(db, author_id)
    if db_response.db_object is None:
        raise db_response.exception
    return db_response.db_object


@app.get("/api/v1/books/{book_id}", response_model=schema.Book)
def get_book_by_id(book_id: int, db=Depends(get_db)):
    db_response = crud_utils.get_book_by_id(db, book_id)
    if db_response.db_object is None:
        raise db_response.exception
    return db_response.db_object


@app.get("/api/v1/books/", response_model=list[schema.Book])
def get_books(skip: int = 0, limit: int = 100, db=Depends(get_db)):
    return crud_utils.get_books(db, skip, limit)


@app.post("/api/v1/books/", response_model=schema.BookCreate)
def create_book(book: schema.BookCreate, db=Depends(get_db)):
    db_response = crud_utils.create_book(db, book)
    if db_response.db_object is None:
        raise db_response.exception
    return db_response.db_object


@app.put("/api/v1/books/{book_id}/", response_model=schema.Book)
def update_book(book_id: int, book: schema.BookUpdate, db=Depends(get_db)):
    db_response = crud_utils.update_book(db, book_id, book)
    if db_response.db_object is None:
        raise db_response.exception
    return db_response.db_object


@app.delete("/api/v1/books/{book_id}/", response_model=schema.Book)
def delete_book(book_id: int, db=Depends(get_db)):
    db_response = crud_utils.delete_book(db, book_id)
    if db_response.db_object is None:
        raise db_response.exception
    return db_response.db_object


@app.put("/api/v1/book_add_copy/{book_id}/", response_model=schema.Book)
def add_book_copy(book_id: int, db=Depends(get_db)):
    db_response = crud_utils.add_book_copy(db, book_id)
    if db_response.db_object is None:
        raise db_response.exception
    return db_response.db_object


@app.put("/api/v1/borrow/{book_id}/", response_model=schema.Book)
def borrow_book(book_id: int, db=Depends(get_db)):
    db_response = crud_utils.borrow_book(db, book_id)
    if db_response.db_object is None:
        raise db_response.exception
    return db_response.db_object


@app.put("/api/v1/return/{book_id}/", response_model=schema.Book)
def return_book(book_id: int, db=Depends(get_db)):
    db_response = crud_utils.return_book(db, book_id)
    if db_response.db_object is None:
        raise db_response.exception
    return db_response.db_object


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=get_app_port())
