import logging
import nest_asyncio # type: ignore
from telegram import Update, Message
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# فعال کردن nest_asyncio
nest_asyncio.apply()

# فعال کردن لاگینگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# آیدی کانال مقصد (کانالی که ربات در آن ادمین است)
TARGET_CHANNEL_ID = '@IntroductionofAirdrop'  # کانال مقصد

# لیستی از کانال‌های مبدا
SOURCE_CHANNEL_USERNAMES = ['@gemz_combo_daily', '@MemefiCode', '@DogMonster']  # کانال‌های مبدا

# تابعی برای پردازش پست‌ها
async def forward_posts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message: Message = update.message

    # ارسال پست به کانال هدف بدون نمایش نام کانال
    if message.text:  # اطمینان از وجود متن در پیام
        # حذف نام کانال‌های مبدا از متن
        modified_text = message.text
        for channel_username in SOURCE_CHANNEL_USERNAMES:
            modified_text = modified_text.replace(channel_username, '').strip()

        # ارسال متن اصلاح شده به کانال مقصد
        await context.bot.send_message(chat_id=TARGET_CHANNEL_ID, text=modified_text)

# راه‌اندازی ربات
async def main() -> None:
    application = ApplicationBuilder().token("8026191420:AAGkIwuskDtU_opshjhY5DRMRP72Gzg5ojU").build()

    # اضافه کردن هندلر برای پیام‌ها از همه کانال‌های مبدا
    for channel_username in SOURCE_CHANNEL_USERNAMES:
        application.add_handler(MessageHandler(filters.TEXT & filters.Chat(username=channel_username), forward_posts))

    # شروع ربات
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
