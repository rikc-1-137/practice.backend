from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "sqlite:///./salon.db"   # для PostgreSQL замените строку подключения

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # нужно только для SQLite
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()