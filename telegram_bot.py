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
SOURCE_CHANNEL_USERNAME = '@gemz_combo_daily'  # کانال مبدا

# تابعی برای پردازش پست‌ها
async def forward_combo_posts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message: Message = update.message

    # بررسی وجود هشتگ #combo در متن پست
    if '#combo' in message.text:
        # حذف لینک‌ها از متن
        modified_text = ' '.join(word for word in message.text.split() if not word.startswith('http'))

        # ارسال پست به کانال هدف
        await context.bot.send_message(chat_id=TARGET_CHANNEL_ID, text=modified_text)

# راه‌اندازی ربات
async def main() -> None:
    application = ApplicationBuilder().token("8026191420:AAGkIwuskDtU_opshjhY5DRMRP72Gzg5ojU").build()

    # اضافه کردن هندلر برای پیام‌ها
    application.add_handler(MessageHandler(filters.TEXT & filters.Chat(username=SOURCE_CHANNEL_USERNAME), forward_combo_posts))

    # شروع ربات
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
