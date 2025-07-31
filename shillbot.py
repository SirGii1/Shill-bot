import logging
import asyncio
import random
from telegram import Update, ForceReply
from telegram.ext import (
    Application, CommandHandler, MessageHandler, ContextTypes, filters
)

# === CONFIGURATION ===
BOT_TOKEN = '7614185922:AAFIZz6uXBuv-w4optpb3XTwTYaWDalsz78'
ADMIN_ID = 2051249497  # Your Telegram user ID

# === VARIABLES ===
shill_messages = ["🚀 Default shill message. Edit me!"]
delay_seconds = 60
shilling_active = False

# === LOGGING ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === SHILL LOOP ===
async def shill_loop(application):
    global shilling_active
    while shilling_active:
        try:
            message = random.choice(shill_messages)
            await application.bot.send_message(chat_id=ADMIN_ID, text=f"📣 {message}")
            await asyncio.sleep(delay_seconds)
        except Exception as e:
            logger.error(f"Shill error: {e}")
            await asyncio.sleep(10)

# === COMMAND HANDLERS ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ Unauthorized.")
        return
    await update.message.reply_text(
        "👋 Welcome to the Shill Bot Admin Panel.\n\n"
        "/add - Add a shill message\n"
        "/list - View all shill messages\n"
        "/setdelay - Set delay time (in seconds)\n"
        "/delay - View current delay\n"
        "/startshill - Start shilling\n"
        "/stopshill - Stop shilling"
    )

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    await update.message.reply_text("✍️ Send the shill message you want to add:")

    async def get_message(msg_update: Update, _: ContextTypes.DEFAULT_TYPE):
        shill_messages.append(msg_update.message.text)
        await msg_update.message.reply_text("✅ Shill message added.")
        application.remove_handler(temp_handler)

    temp_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), get_message)
    application.add_handler(temp_handler, 1)

async def list_msgs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    msg = "\n".join([f"{i+1}. {m}" for i, m in enumerate(shill_messages)])
    await update.message.reply_text(f"📜 Shill Messages:\n{msg}")

async def set_delay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    await update.message.reply_text("⏱️ Send the new delay time (in seconds):")

    async def receive_delay(msg_update: Update, _: ContextTypes.DEFAULT_TYPE):
        global delay_seconds
        try:
            delay_seconds = int(msg_update.message.text)
            await msg_update.message.reply_text(f"✅ Delay set to {delay_seconds}s")
        except:
            await msg_update.message.reply_text("❌ Invalid number.")
        application.remove_handler(temp_handler)

    temp_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), receive_delay)
    application.add_handler(temp_handler, 1)

async def get_delay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    await update.message.reply_text(f"⏱️ Current delay: {delay_seconds}s")

async def start_shilling(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global shilling_active
    if update.effective_user.id != ADMIN_ID:
        return
    if not shilling_active:
        shilling_active = True
        await update.message.reply_text("🚀 Shilling started!")
        asyncio.create_task(shill_loop(application))
    else:
        await update.message.reply_text("⚠️ Shilling already running.")

async def stop_shilling(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global shilling_active
    if update.effective_user.id != ADMIN_ID:
        return
    shilling_active = False
    await update.message.reply_text("🛑 Shilling stopped.")

# === BOT SETUP ===
application = Application.builder().token(BOT_TOKEN).build()

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("add", add))
application.add_handler(CommandHandler("list", list_msgs))
application.add_handler(CommandHandler("setdelay", set_delay))
application.add_handler(CommandHandler("delay", get_delay))
application.add_handler(CommandHandler("startshill", start_shilling))
application.add_handler(CommandHandler("stopshill", stop_shilling))

if __name__ == '__main__':
    application.run_polling()
