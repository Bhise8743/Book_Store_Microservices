from sqlalchemy.orm import declarative_base, Session
from sqlalchemy import BigInteger, Integer, String, Column, create_engine, Boolean

from User.setting import setting

engine = create_engine(f'postgresql+psycopg2://postgres:{setting.postgresSQL_password}@localhost:5432/{setting.user_database_name}')
session = Session(engine)
Base = declarative_base()

def get_db():
    db = session
    try:
        yield db
    finally:
        db.close()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String(50), nullable=False, unique=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    phone = Column(BigInteger, nullable=False)
    password = Column(String(256), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    is_verified = Column(Boolean, default=False)
    is_super_user = Column(Boolean, default=False)
