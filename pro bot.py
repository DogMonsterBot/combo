import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# توکن ربات
BOT_TOKEN = '8026191420:AAGkIwuskDtU_opshjhY5DRMRP72Gzg5ojU'

# شناسه گروه مقصد
TARGET_GROUP_ID = '@IntroductionofAirdrop'

# هشتگ‌های مورد نظر
TAGS = ['#tag1', '#tag2', '#tag3']  # اینجا می‌توانید هشتگ‌های دلخواه خود را اضافه کنید

# راه‌اندازی logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# تابع برای پردازش پیام‌ها
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # چک کردن اینکه آیا پیام شامل هشتگ‌های مشخص شده است
    if any(tag in update.message.text for tag in TAGS):
        # حذف لینک‌ها از متن
        text = update.message.text
        text_without_links = ' '.join(word for word in text.split() if not word.startswith('http'))

        try:
            # ارسال متن یا تصویر به گروه مقصد
            if update.message.photo:  # چک کردن وجود تصویر
                await context.bot.send_photo(chat_id=TARGET_GROUP_ID, photo=update.message.photo[-1].file_id, caption=text_without_links)
            else:
                await context.bot.send_message(chat_id=TARGET_GROUP_ID, text=text_without_links)

            logging.info(f"Message sent to target group: {text_without_links}")
        except Exception as e:
            logging.error(f"Failed to send message: {e}")

# تابع اصلی
async def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # افزودن هندلر برای پیام‌ها
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    application.add_handler(MessageHandler(filters.PHOTO, handle_message))  # اضافه کردن هندلر برای تصاویر

    # شروع polling
    await application.run_polling()

if __name__ == '__main__':
    import asyncio  # فقط در اینجا وارد کنید

    # ثبت شروع ربات
    logging.info("Starting the bot...")
    
    # استفاده از حلقه‌ی رویداد در حال اجرا
    asyncio.run(main())
