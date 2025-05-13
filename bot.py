import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from yt_dlp import YoutubeDL
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client("youtube_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# /start komandasi
@app.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    await message.reply(
        "👋 Salom!\n\n"
        "Men YouTube havolalaringizdan videoni yoki audioni yuklab beraman.\n"
        "📥 Havolani yuboring va formatni tanlang."
    )

# Link kelganda format tanlovi
@app.on_message(filters.text & filters.private)
async def handle_link(client: Client, message: Message):
    url = message.text.strip()
    if not url.startswith("http"):
        return await message.reply("📎 Iltimos, YouTube havolasini yuboring.")

    buttons = [
        [
            InlineKeyboardButton("🎥 Video", callback_data=f"video|{url}"),
            InlineKeyboardButton("🎧 Audio", callback_data=f"audio|{url}")
        ]
    ]
    await message.reply(
        "📤 Yuklab olish formatini tanlang:",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# Media yuklab olish funksiyasi
def download_media(url, media_type):
    if media_type == "audio":
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/%(title).30s.%(ext)s',
            'noplaylist': True,
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    else:
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': 'downloads/%(title).30s.%(ext)s',
            'noplaylist': True,
            'quiet': True,
            'merge_output_format': 'mp4',
        }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if media_type == 'audio':
                filename = filename.rsplit('.', 1)[0] + '.mp3'
            return filename, info.get("title", "Fayl")
    except Exception as e:
        print("Xatolik:", e)
        return None, None

# Tugma bosilganda
@app.on_callback_query()
async def handle_callback(client: Client, callback_query: CallbackQuery):
    await callback_query.answer()
    action, url = callback_query.data.split("|", 1)

    # Tugmali xabarni yangilab o‘chirish
    await callback_query.message.edit_text("⏳ Yuklab olinmoqda...")

    loop = asyncio.get_event_loop()
    filepath, title = await loop.run_in_executor(None, download_media, url, action)

    if filepath and os.path.exists(filepath):
        try:
            if action == "audio":
                await callback_query.message.reply_audio(audio=filepath, caption=f"✅ Yuklandi: {title}")
            else:
                await callback_query.message.reply_video(video=filepath, caption=f"✅ Yuklandi: {title}")
        except Exception as e:
            await callback_query.message.edit_text(f"❌ Xatolik: {str(e)}")
        finally:
            os.remove(filepath)
    else:
        await callback_query.message.edit_text("❌ Yuklab bo‘lmadi. Havola noto‘g‘ri yoki qo‘llab-quvvatlanmaydi.")

# Papkani yaratib qo'yamiz
os.makedirs("downloads", exist_ok=True)

app.run()
