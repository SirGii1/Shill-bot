import asyncio
import logging
import random
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# === SETTINGS ===
BOT_TOKEN = '7614185922:AAFIZz6uXBuv-w4optpb3XTwTYaWDalsz78'  # Your bot token
ADMIN_ID = 2051249497  # Your Telegram user ID

# === GLOBAL VARIABLES ===
shill_messages = ["🚀 Welcome to $DONT! Edit this with /add"]
delay_seconds = 60
shill_running = False

# === LOGGING ===
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

# === HANDLERS ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ You are not authorized.")
        return

    await update.message.reply_text(
        "🛠 Admin Panel\n\n"
        "/add - Add new shill message\n"
        "/list - Show messages\n"
        "/setdelay - Set timer delay (in seconds)\n"
        "/delay - Show current delay\n"
        "/startshill - Start shilling\n"
        "/stopshill - Stop shilling"
    )

async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    await update.message.reply_text("✍️ Send the new shill message:")

    async def get_msg(msg_update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        msg = msg_update.message.text
        shill_messages.append(msg)
        await msg_update.message.reply_text("✅ Message added.")
        app.remove_handler(temp_handler)

    temp_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, get_msg)
    app.add_handler(temp_handler, 1)

async def list_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    if not shill_messages:
        await update.message.reply_text("📭 No shill messages yet.")
        return

    reply = "\n".join([f"{i+1}. {msg}" for i, msg in enumerate(shill_messages)])
    await update.message.reply_text(f"📜 Current Messages:\n{reply}")

async def set_delay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return

    await update.message.reply_text("⏱️ Send new delay time in seconds:")

    async def get_delay(msg_update: Update, ctx: ContextTypes.DEFAULT_TYPE):
        global delay_seconds
        try:
            delay_seconds = int(msg_update.message.text)
            await msg_update.message.reply_text(f"✅ Delay set to {delay_seconds} seconds.")
        except:
            await msg_update.message.reply_text("❌ Invalid input. Try again.")
        app.remove_handler(temp_handler)

    temp_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, get_delay)
    app.add_handler(temp_handler, 1)

async def show_delay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    await update.message.reply_text(f"⏱️ Current delay: {delay_seconds} seconds")

async def start_shilling(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global shill_running
    if update.effective_user.id != ADMIN_ID:
        return
    if shill_running:
        await update.message.reply_text("⚠️ Already shilling!")
        return

    await update.message.reply_text("🚀 Starting shill...")
    shill_running = True
    asyncio.create_task(shill_loop(context.application))

async def stop_shilling(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global shill_running
    if update.effective_user.id != ADMIN_ID:
        return
    shill_running = False
    await update.message.reply_text("🛑 Shilling stopped.")

async def shill_loop(app):
    global shill_running
    while shill_running:
        try:
            msg = random.choice(shill_messages)
            await app.bot.send_message(chat_id=ADMIN_ID, text=f"📣 {msg}")
            await asyncio.sleep(delay_seconds)
        except Exception as e:
            logging.error(f"Error: {e}")
            await asyncio.sleep(5)

# === MAIN SETUP ===
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add))
app.add_handler(CommandHandler("list", list_messages))
app.add_handler(CommandHandler("setdelay", set_delay))
app.add_handler(CommandHandler("delay", show_delay))
app.add_handler(CommandHandler("startshill", start_shilling))
app.add_handler(CommandHandler("stopshill", stop_shilling))

if __name__ == "__main__":
    print("✅ Bot is running... Press Ctrl+C to stop")
    app.run_polling()
