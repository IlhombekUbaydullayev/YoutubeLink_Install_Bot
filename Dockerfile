# Eng yengil va zamonaviy Python image
FROM python:3.12-slim

# Tizim yangilanishi va kerakli tizim kutubxonalari
RUN apt-get update && apt-get install -y \
    ffmpeg \
 && rm -rf /var/lib/apt/lists/*

# Ishchi katalogni yaratish
WORKDIR /app

# Fayllarni konteynerga ko‘chirish
COPY . .

# Python kutubxonalarini o‘rnatish
RUN pip install --no-cache-dir -r requirements.txt

# downloads papkasini avtomatik yaratish
RUN mkdir -p downloads

# Botni ishga tushirish
CMD ["python", "bot.py"]
