# Python rasmiy image
FROM python:3.12-slim

# Environment sozlamalar
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Ishchi papka
WORKDIR /app

# Sistemaga kerakli paketlar (agar kerak bo‘lsa)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# requirements.txt ni ko‘chiramiz
COPY requirements.txt .

# Python kutubxonalarni o‘rnatamiz
RUN pip install --no-cache-dir -r requirements.txt

# Barcha fayllarni ko‘chiramiz
COPY . .

# Botni ishga tushirish
CMD ["python", "bot.py"]