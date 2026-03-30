FROM python:3.9-slim

WORKDIR /app

# تثبيت المتطلبات
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ الملفات
COPY . .

# فتح المنفذ
EXPOSE 8501

# تشغيل التطبيق
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]