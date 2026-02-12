import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# تنظیمات Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash') # نسخه سریع و رایگان

def process_expense_text(text: str):
    prompt = f"""
    Extract expense details from this text: "{text}"
    Return ONLY a JSON object with these keys: "title", "amount", "category".
    Categories: Food, Transport, Travel, Rent, Shopping, Others.
    If amount not found, use 0.
    Example: "Spent 5€ on coffee" -> {{"title": "Coffee", "amount": 5, "category": "Food"}}
    """
    
    response = model.generate_content(prompt)
    
    # تمیز کردن پاسخ (گاهی جمینای مارک‌آپ ```json اضافه می‌کند)
    clean_json = response.text.replace('```json', '').replace('```', '').strip()
    
    return json.loads(clean_json)

def get_ai_insight(summary_data: dict):
    prompt = f"Based on this spending data: {summary_data}, give a 1-sentence financial advice in English."
    
    # اینجا از همان مدلی که در مرحله قبل استفاده کردی (Gemini 2.0) استفاده کن
    # خروجی یک جمله مشاوره باشد
    response = model.generate_content(prompt) # فرض بر اینکه مدل را تعریف کردی
    return response.text