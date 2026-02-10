import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# این خط باعث می‌شود اطلاعات فایل .env خوانده شود
load_dotenv()

# آدرس دیتابیس را از فایل مخفی برمی‌داریم
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# ایجاد موتور اتصال
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)