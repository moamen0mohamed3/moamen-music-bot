import os
import asyncio
from pyrogram import Client, filters
import yt_dlp


API_ID = 35699337
 
API_HASH = "99dbf216ac9242d7cfea317abd350fd8"

BOT_TOKEN = "8393428904:AAHN8ttOouaKxICTsmSDYEvaOIR3_rUOXko" 
# ----------------------

app = Client("music_downloader", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


ydl_opts = {
    'format': 'bestaudio/best',
    'default_search': 'ytsearch',
    'noplaylist': True,
    'outtmpl': '%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'quiet': True,
}

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        "👋 أهلاً بك في بوت تحميل الأغاني!\n\n"
        "فقط أرسل لي **اسم الأغنية** وسأقوم بالبحث عنها وإرسالها لك كملف صوتي."
    )

@app.on_message(filters.text & filters.private)
async def download_song(client, message):
    query = message.text
    status_msg = await message.reply_text(f"🔍 جاري البحث عن: {query}...")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"ytsearch:{query}", download=True)['entries'][0]
            # اسم الملف بعد التحويل لـ mp3
            file_path = ydl.prepare_filename(info).rsplit('.', 1)[0] + ".mp3"
            title = info.get('title', 'Unknown Title')
            duration = info.get('duration', 0)

        await status_msg.edit("📤 جاري رفع الملف إلى تلجرام...")
        
        # إرسال الملف الصوتي
        await message.reply_audio(
            audio=open(file_path, 'rb'),
            caption=f"🎵 **{title}**",
            duration=int(duration)
        )
        
        await status_msg.delete()

        # مسح الملف من ذاكرة الهاتف لتوفير المساحة
        if os.path.exists(file_path):
            os.remove(file_path)

    except Exception as e:
        await status_msg.edit(f"❌ حدث خطأ أثناء التحميل: {str(e)}")
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)

print("✅ البوت يعمل الآن بنجاح...")
app.run()
