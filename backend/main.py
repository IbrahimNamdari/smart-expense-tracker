from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, schemas, database
from ai_processor import process_expense_text
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ساخت جدول‌ها (اگر قبلا ساخته نشده باشند)
models.Base.metadata.create_all(bind=database.engine)

# تابع کمکی برای وصل شدن به دیتابیس
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "API is running!"}

# ۱. ذخیره هزینه جدید
@app.post("/expenses/", response_model=schemas.ExpenseResponse)
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    db_expense = models.Expense(**expense.dict())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense

# ۲. دریافت لیست تمام هزینه‌ها
@app.get("/expenses/")
def read_expenses(db: Session = Depends(get_db)):
    return db.query(models.Expense).all()

@app.post("/expenses/ai/")
def create_expense_via_ai(text_input: str, db: Session = Depends(get_db)):
    # 1. استفاده از هوش مصنوعی برای فهمیدن جزئیات
    ai_data = process_expense_text(text_input)
    
    # 2. ذخیره در دیتابیس
    db_expense = models.Expense(
        title=ai_data['title'],
        amount=ai_data['amount'],
        category=ai_data['category']
    )
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return {"message": "AI processed successfully", "data": db_expense}

@app.get("/expenses/summary/")
def get_summary(db: Session = Depends(get_db)):
    # 1. دریافت همه داده‌ها از دیتابیس
    expenses = db.query(models.Expense).all()
    if not expenses:
        return {"message": "No data available"}

    # 2. تبدیل داده‌ها به یک DataFrame (ساختار دیتاساینسی)
    df = pd.DataFrame([
        {"category": e.category, "amount": e.amount} for e in expenses
    ])

    # 3. گروه‌بندی بر اساس دسته‌بندی و جمع مبالغ
    summary = df.groupby("category")["amount"].sum().to_dict()
    
    return summary