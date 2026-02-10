from sqlalchemy import create_url
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# آدرس دیتابیس (بعدا این را در فایل .env میگذاریم)
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/expense_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)