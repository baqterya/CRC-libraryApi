from typing import Any

from fastapi import HTTPException
from sqlalchemy import select, insert
from sqlalchemy.orm import Session
import app.models as models
import app.schema as schema


class DBResponse:
    def __init__(self, db_object: Any, error_message: str = None, status_code: int = None):
        self.db_object = db_object
        self.exception = HTTPException(status_code=status_code, detail=error_message) if error_message else None


def get_author_by_id(db: Session, author_id: int) -> DBResponse:
    db_author = db.scalars(select(models.AuthorModel).where(models.AuthorModel.id == author_id)).first()
    if db_author is None:
        return DBResponse(None, f"Author with id {author_id} not found", 404)
    return DBResponse(db_author)


def get_author_by_name(db: Session, author_name_last: str, author_name_first: str) -> DBResponse:
    db_author = db.scalars(select(models.AuthorModel).where(
        models.AuthorModel.name_last == author_name_last,
        models.AuthorModel.name_first == author_name_first
    )).first()
    if db_author is None:
        return DBResponse(None, f"Author with name '{author_name_last} {author_name_first}' not found", 404)
    return DBResponse(db_author)


def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.scalars(select(models.AuthorModel).offset(skip).limit(limit)).all()


def create_author(db: Session, author: schema.AuthorCreate) -> DBResponse:
    db_response = get_author_by_name(db, author.name_last, author.name_first)
    if db_response.db_object:
        return DBResponse(None, f"Author with name '{author.name_last} {author.name_first}' already exists", 400)
    db_author = models.AuthorModel(**author.dict())
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return DBResponse(db_author)


def update_author(db: Session, author_id: int, author: schema.AuthorUpdate) -> DBResponse:
    db_response = get_author_by_id(db, author_id)
    if db_response.db_object is None:
        return db_response
    for key, value in author.dict().items():
        setattr(db_response.db_object, key, value)
    db.commit()
    db.refresh(db_response.db_object)
    return db_response


def delete_author(db: Session, author_id: int) -> DBResponse:
    db_response = get_author_by_id(db, author_id)
    if db_response.db_object is None:
        return db_response
    db.delete(db_response.db_object)
    db.commit()
    return db_response


def get_book_by_id(db: Session, book_id: int) -> DBResponse:
    db_book = db.scalars(select(models.BookModel).where(models.BookModel.id == book_id)).first()
    if db_book is None:
        return DBResponse(None, f"Book with id {book_id} not found", 404)
    return DBResponse(db_book)


def get_book_by_title(db: Session, book_title: str) -> DBResponse:
    db_book = db.scalars(select(models.BookModel).where(models.BookModel.title == book_title)).first()
    if db_book is None:
        return DBResponse(None, f"Book with title '{book_title}' not found", 404)
    return DBResponse(db_book)


def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.scalars(select(models.BookModel).offset(skip).limit(limit)).all()


def create_book(db: Session, book: schema.BookCreate) -> DBResponse:
    db_response = get_book_by_title(db, book.title)
    if db_response.db_object:
        return DBResponse(None, f"Book with title '{book.title}' already exists", 400)
    db_book = models.BookModel(**book.dict())
    db_book.amount_currently_borrowed = 0
    db_book.borrow_history = ""
    db_book.is_available = True
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return DBResponse(db_book)


def update_book(db: Session, book_id: int, book: schema.BookUpdate) -> DBResponse:
    db_response = get_book_by_id(db, book_id)
    if db_response.db_object is None:
        return db_response
    for key, value in book.dict().items():
        setattr(db_response.db_object, key, value)
    db.commit()
    db.refresh(db_response.db_object)
    return db_response


def delete_book(db: Session, book_id: int) -> DBResponse:
    db_response = get_book_by_id(db, book_id)
    if db_response.db_object is None:
        return db_response
    db.delete(db_response.db_object)
    db.commit()
    return db_response


def add_book_copy(db: Session, book_id: int) -> DBResponse:
    db_response = get_book_by_id(db, book_id)
    if db_response.db_object is None:
        return db_response
    db_response.db_object.add_copy()
    db.commit()
    db.refresh(db_response.db_object)
    return db_response


def borrow_book(db: Session, book_id: int) -> DBResponse:
    db_response = get_book_by_id(db, book_id)
    if db_response.db_object is None:
        return db_response
    if db_response.db_object.is_available:
        db_response.db_object.borrow()
        db.commit()
        db.refresh(db_response.db_object)
    else:
        db_response = DBResponse(None, "Book is not available", 400)
    return db_response


def return_book(db: Session, book_id: int) -> DBResponse:
    db_response = get_book_by_id(db, book_id)
    if db_response.db_object is None:
        return DBResponse(None, "Book not found", 404)
    if db_response.db_object.amount_currently_borrowed == 0:
        return DBResponse(None, "Book is not borrowed", 400)
    db_response.db_object.return_()
    db.commit()
    db.refresh(db_response.db_object)
    return db_response
