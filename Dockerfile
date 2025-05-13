# 1. Python bazasidan boshlaymiz
FROM python:3.10-slim

# 2. Ishchi katalogni yaratamiz
WORKDIR /app

# 3. Tizim kutubxonalarini o‘rnatamiz (yt-dlp uchun kerak bo‘lishi mumkin)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 4. Fayllarni konteynerga nusxalash
COPY . .

# 5. Talab qilinadigan kutubxonalarni o‘rnatish
RUN pip install --no-cache-dir -r requirements.txt

# 6. downloads papkasini yaratish (agar mavjud bo‘lmasa)
RUN mkdir -p downloads

# 7. Botni ishga tushirish
CMD ["python", "bot.py"]
