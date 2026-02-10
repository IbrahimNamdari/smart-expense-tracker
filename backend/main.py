from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models, schemas, database

app = FastAPI()

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