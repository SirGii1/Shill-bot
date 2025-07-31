import asyncio
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

# === CONFIGURATION ===
BOT_TOKEN = '7614185922:AAFIZz6uXBuv-w4optpb3XTwTYaWDalsz78'
ADMIN_ID = 2051249497

# === BOT STATE ===
shill_messages = ["🚀 Welcome to $DONT!"]
delay_seconds = 60
shill_running = False
waiting_for = None  # Keeps track of what input is expected (e.g. 'add' or 'delay')

# === PANEL KEYBOARD ===
def get_admin_panel():
    keyboard = [
        [InlineKeyboardButton("➕ Add Message", callback_data="add")],
        [InlineKeyboardButton("📝 View Messages", callback_data="list")],
        [InlineKeyboardButton("⏱ Set Delay", callback_data="set_delay")],
        [InlineKeyboardButton("▶️ Start Shill", callback_data="start_shill")],
        [InlineKeyboardButton("⏹ Stop Shill", callback_data="stop_shill")],
        [InlineKeyboardButton("⏱ View Delay", callback_data="view_delay")],
    ]
    return InlineKeyboardMarkup(keyboard)

# === START HANDLER ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ You are not authorized.")
        return

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text="👋 Welcome to your Shill Bot Admin Panel:",
        reply_markup=get_admin_panel()
    )

# === CALLBACK HANDLER ===
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global waiting_for, shill_running

    query = update.callback_query
    await query.answer()

    if query.from_user.id != ADMIN_ID:
        await query.edit_message_text("❌ You're not authorized.")
        return

    data = query.data

    if data == "add":
        waiting_for = "add"
        await query.edit_message_text("✍️ Send the shill message you want to add:")
    elif data == "list":
        msg_list = "\n".join([f"{i+1}. {m}" for i, m in enumerate(shill_messages)])
        await query.edit_message_text(f"📜 Current messages:\n\n{msg_list}", reply_markup=get_admin_panel())
    elif data == "set_delay":
        waiting_for = "delay"
        await query.edit_message_text("⏱️ Send the new delay time in seconds:")
    elif data == "view_delay":
        await query.edit_message_text(f"⏱️ Current delay: {delay_seconds} seconds", reply_markup=get_admin_panel())
    elif data == "start_shill":
        if shill_running:
            await query.edit_message_text("⚠️ Shilling already running.", reply_markup=get_admin_panel())
        else:
            shill_running = True
            await query.edit_message_text("🚀 Shilling started!", reply_markup=get_admin_panel())
            asyncio.create_task(shill_loop(context))
    elif data == "stop_shill":
        shill_running = False
        await query.edit_message_text("🛑 Shilling stopped.", reply_markup=get_admin_panel())

# === TEXT INPUT HANDLER ===
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global waiting_for, delay_seconds

    if update.effective_user.id != ADMIN_ID:
        return

    text = update.message.text

    if waiting_for == "add":
        shill_messages.append(text)
        await update.message.reply_text("✅ Message added.", reply_markup=get_admin_panel())
    elif waiting_for == "delay":
        try:
            delay_seconds = int(text)
            await update.message.reply_text(f"✅ Delay set to {delay_seconds} seconds.", reply_markup=get_admin_panel())
        except:
            await update.message.reply_text("❌ Invalid number. Please try again.", reply_markup=get_admin_panel())

    waiting_for = None

# === SHILL LOOP ===
async def shill_loop(context):
    global shill_running
    while shill_running:
        try:
            msg = random.choice(shill_messages)
            await context.bot.send_message(chat_id=ADMIN_ID, text=f"📣 {msg}")
            await asyncio.sleep(delay_seconds)
        except Exception as e:
            await context.bot.send_message(chat_id=ADMIN_ID, text=f"❌ Error: {e}")
            await asyncio.sleep(10)

# === SETUP BOT ===
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

if __name__ == "__main__":
    print("✅ Bot is running...")
    app.run_polling()
