from sqlalchemy.orm import Session, declarative_base
from sqlalchemy import Column, Integer, BigInteger, String, create_engine
from Book.setting import setting

engine = create_engine(f'postgresql+psycopg2://postgres:{setting.postgresSQL_password}@localhost:5432/{setting.book_database_name}')
session = Session(engine)
Base = declarative_base()


def get_db():
    db = session
    try:
        yield db
    finally:
        db.close()


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    book_name = Column(String, nullable=False)
    author = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)

# alembic -c alembic.book.ini revision --autogenerate -m "init book model"
# alembic -c alembic.book.ini upgrade head
