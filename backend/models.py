from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class Expense(Base):
    __tablename__ = "expenses" # نام جدول در دیتابیس

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String) # مثلا: خرید از استارباکس
    amount = Column(Float) # مبلغ: 5.20
    category = Column(String) # دسته بندی: Food
    date = Column(DateTime, default=datetime.datetime.utcnow) # زمان ثبت