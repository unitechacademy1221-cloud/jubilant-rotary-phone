import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "7903709601:AAF4XEUzGHQueTe5CQvfJ8Wp0Iwf-1LeoCw"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Instagram videosini yuboring — men uni yuklab beraman.")

async def download_instagram_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if "instagram.com" not in url:
        await update.message.reply_text("❗ Instagram havolasi yuboring.")
        return

    await update.message.reply_text("⏳ Yuklab olinmoqda...")

    try:
        ydl_opts = {
            'outtmpl': 'video.%(ext)s',
            'format': 'mp4',
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_path = ydl.prepare_filename(info)

        with open(video_path, 'rb') as f:
            await update.message.reply_video(f)

        os.remove(video_path)

    except Exception as e:
        await update.message.reply_text(f"Xatolik: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_instagram_video))
    print("Bot ishga tushdi.")
    app.run_polling()
