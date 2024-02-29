from sqlalchemy.orm import Session, declarative_base
from sqlalchemy import Column, Integer, String, create_engine, Boolean

from Cart.setting import setting

engine = create_engine(
    f'postgresql+psycopg2://postgres:{setting.postgresSQL_password}@localhost:5432/{setting.cart_database_name}')
session = Session(engine)
Base = declarative_base()


def get_db():
    db = session
    try:
        yield db
    finally:
        db.close()


class Cart(Base):
    __tablename__ = 'cart'
    id = Column(Integer, primary_key=True, index=True)
    total_quantity = Column(Integer, nullable=False, default=0)
    total_price = Column(Integer, nullable=False, default=0)
    user_id = Column(Integer, nullable=False)


class CartItems(Base):
    __tablename__ = 'cart_items'
    id = Column(Integer, primary_key=True, index=True)
    price = Column(Integer, nullable=False, default=0)
    quantity = Column(Integer, nullable=False, default=0)
    book_id = Column(Integer, nullable=False)
    cart_id = Column(Integer, nullable=False)
