import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from googletrans import Translator

# تنظیمات لاگینگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# توکن ربات و آیدی کانال‌ها
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8026191420:AAGkIwuskDtU_opshjhY5DRMRP72Gzg5ojU")
SOURCE_CHANNEL_IDS = ['-1002215159433', '-1002490406722']  # آیدی کانال مبدا
TARGET_CHANNEL_ID = '-1002248091563'  # آیدی کانال مقصد

# تابع برای پردازش پیام
async def process_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.channel_post:
        message = update.channel_post.text or ""
        # ترجمه متن
        translator = Translator()
        translated = translator.translate(message, dest='fa')
        # ارسال به کانال مقصد
        await context.bot.send_message(chat_id=TARGET_CHANNEL_ID, text=translated.text)

# تابع اصلی
async def main():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    for channel_id in SOURCE_CHANNEL_IDS:
        application.add_handler(MessageHandler(filters.TEXT & filters.Chat(channel_id), process_message))

    # شروع ربات
    await application.run_polling()

if __name__ == '__main__':
    import asyncio

    # استفاده از asyncio.run() به جای get_event_loop
    try:
        asyncio.run(main())
    except RuntimeError as e:
        print(f"خطا: {e}")
