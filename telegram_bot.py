import logging
from telegram import Update, Message
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# فعال کردن لاگینگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# آیدی کانال مقصد (کانالی که ربات در آن ادمین است)
TARGET_CHANNEL_ID = '@IntroductionofAirdrop'  # کانال مقصد
SOURCE_CHANNEL_USERNAME = '@MemefiCode'  # کانال مبدا

# تابعی برای پردازش پست‌ها
async def forward_posts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message: Message = update.message

    # ارسال پست به کانال هدف بدون نمایش نام کانال
    if message.text:  # اطمینان از وجود متن در پیام
        # حذف نام کانال (در صورت وجود) و ارسال متن
        modified_text = message.text.replace(SOURCE_CHANNEL_USERNAME, '').strip()
        await context.bot.send_message(chat_id=TARGET_CHANNEL_ID, text=modified_text)

# راه‌اندازی ربات
async def main() -> None:
    application = ApplicationBuilder().token("8026191420:AAGkIwuskDtU_opshjhY5DRMRP72Gzg5ojU").build()

    # اضافه کردن هندلر برای پیام‌ها
    application.add_handler(MessageHandler(filters.TEXT & filters.Chat(username=SOURCE_CHANNEL_USERNAME), forward_posts))

    # شروع ربات
    await application.run_polling()

if __name__ == '__main__':
    import asyncio

    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
