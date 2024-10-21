import asyncio
import re
import logging
from deep_translator import GoogleTranslator
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

import nest_asyncio  # اضافه کردن nest_asyncio برای حل مشکل حلقه رویداد
nest_asyncio.apply()  # اعمال تنظیمات

# تنظیمات ورود به سیستم
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# توکن ربات
TOKEN = '8026191420:AAGkIwuskDtU_opshjhY5DRMRP72Gzg5ojU'

# آیدی کانال‌های مبدا و مقصد
SOURCE_CHANNEL_IDS = [
    '7320989848',      # آیدی کانال مبدا اول
    '-1002215159433',  # آیدی کانال مبدا دوم
    '-1002490406722',  # آیدی کانال مبدا سوم
]
TARGET_CHANNEL_ID = '-1002248091563'  # آیدی کانال مقصد را اینجا وارد کنید

# تابع حذف لینک‌ها از متن
def remove_links(text):
    return re.sub(r'http\S+', '', text)

# تابع ترجمه متن به فارسی
def translate_to_persian(text):
    translated = GoogleTranslator(source='auto', target='fa').translate(text)
    return translated

# تابع پردازش پیام
async def process_message(update: Update, context):
    # چک کردن اینکه پیام از یکی از کانال‌های مبدا باشد
    if update.channel_post and str(update.channel_post.chat_id) in SOURCE_CHANNEL_IDS:
        # حذف لینک‌ها از پیام
        text_without_links = remove_links(update.channel_post.text)

        # ترجمه به فارسی
        translated_text = translate_to_persian(text_without_links)

        # ارسال پیام ترجمه‌شده به کانال مقصد
        await context.bot.send_message(chat_id=TARGET_CHANNEL_ID, text=translated_text)

# دستور /start برای شروع کار ربات
async def start(update: Update, context):
    await update.message.reply_text('سلام! این ربات آماده است تا پست‌های کانال مبدا را پردازش کرده و به کانال مقصد ارسال کند.')

# تابع اصلی
async def main():
    # ایجاد اپلیکیشن تلگرام با استفاده از توکن
    application = ApplicationBuilder().token(TOKEN).build()

    # تنظیم هندلرها
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.ALL, process_message))

    # اجرای ربات
    await application.run_polling()

# تابعی برای اجرا در محیط‌های با حلقه رویداد فعال
def run_bot():
    asyncio.run(main())  # اجرای تابع اصلی

# اجرای برنامه
if __name__ == '__main__':
    run_bot()
