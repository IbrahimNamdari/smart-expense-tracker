from fastapi import FastAPI
import models
from database import engine

app = FastAPI()

# این خط جادویی است: تمام مدل‌هایی که در models.py ساختی را در دیتابیس آنلاین می‌سازد
models.Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Welcome to AI Expense Tracker API!"}