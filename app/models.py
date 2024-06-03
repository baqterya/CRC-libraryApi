from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Date, func, Boolean, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class AuthorModel(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name_last = Column(String)
    name_first = Column(String)
    date_birth = Column(Date)
    date_death = Column(Date, nullable=True)
    country_of_birth = Column(String)

    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    books = relationship('BookModel', back_populates='author')


class BookModel(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String)
    year_published = Column(Integer)
    isbn = Column(String)
    language = Column(String)
    amount_total = Column(Integer)
    amount_currently_borrowed = Column(Integer)
    borrow_history = Column(String)
    is_available = Column(Boolean)

    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())

    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship('AuthorModel', back_populates='books')

    def last_borrowed(self) -> str:
        return self.borrow_history.split(',')[-1]

    def borrowed_ever(self) -> int:
        return len(self.borrow_history.split(','))

    def borrow(self):
        self.amount_currently_borrowed += 1
        if self.amount_currently_borrowed == self.amount_total:
            self.is_available = False
        self.borrow_history += f",{datetime.now()}"

    def return_(self):
        self.amount_currently_borrowed -= 1
        if not self.is_available and self.amount_currently_borrowed < self.amount_total:
            self.is_available = True

    def add_copy(self):
        self.amount_total += 1
        if self.amount_currently_borrowed < self.amount_total:
            self.is_available = True
