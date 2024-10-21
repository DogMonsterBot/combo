import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# توکن ربات
BOT_TOKEN = '8026191420:AAGkIwuskDtU_opshjhY5DRMRP72Gzg5ojU'

# شناسه کانال مبدا و مقصد
SOURCE_CHANNEL_IDS = [
    '7320989848',
    '-1002215159433',
    '-1002490406722'
]
TARGET_CHANNEL_ID = '-1002248091563'

# راه‌اندازی logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# تابع برای پردازش پیام‌ها
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # چک کردن اینکه آیا پیام از کانال مبدا آمده است
    if str(update.message.chat.id) in SOURCE_CHANNEL_IDS:
        # حذف لینک‌ها از متن
        text = update.message.text
        text_without_links = ' '.join(word for word in text.split() if not word.startswith('http'))

        try:
            # ارسال به کانال مقصد
            await context.bot.send_message(chat_id=TARGET_CHANNEL_ID, text=text_without_links)
            logging.info(f"Message sent to target channel: {text_without_links}")
        except Exception as e:
            logging.error(f"Failed to send message: {e}")

# تابع اصلی
async def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # افزودن هندلر برای پیام‌ها
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    # شروع polling
    await application.run_polling()

if __name__ == '__main__':
    import asyncio  # فقط در اینجا وارد کنید

    # ثبت شروع ربات
    logging.info("Starting the bot...")

    # استفاده از حلقه‌ی رویداد در حال اجرا
    asyncio.run(main())
