import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

GROUP_LINK = "https://t.me/+NJLTREq5F6E4NWE0"
REGISTER_LINK = "https://grindpoint.com.ng/register"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

WELCOME_TEXT = """Hello 👋

Welcome on board!

To get started:
1. Join our Telegram group for updates and support
2. Create your free account on Grindpoint

Once you’re registered, you can start completing tasks and earning real Naira.

If you need any help, just tap the button below.

Welcome to the Grindpoint family 🔥"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 Join Telegram Group", url=GROUP_LINK)],
        [InlineKeyboardButton("📝 Create Free Account", url=REGISTER_LINK)],
        [InlineKeyboardButton("🆘 I Need Help", callback_data="need_help")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(WELCOME_TEXT, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "need_help":
        await query.message.reply_text(
            "Okay, I’ve received your request ✅\n\nA human support agent will get back to you shortly.\nPlease describe your problem."
        )

        user = query.from_user
        username = f"@{user.username}" if user.username else "No username"
        text = f"🆘 *New Support Request*\n\nFrom: {user.full_name}\nUsername: {username}\nUser ID: `{user.id}`\n\nThey clicked *I Need Help*"
        await context.bot.send_message(chat_id=ADMIN_ID, text=text, parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text.strip().lower()

    if text in ["hi", "hello", "hey", "good morning", "good evening", "start", "help"]:
        await start(update, context)
        return

    await update.message.reply_text(
        "Thank you for your message.\n\nA human support agent will get back to you shortly. Please wait."
    )

    username = f"@{user.username}" if user.username else "No username"
    msg = f"💬 *New Message*\n\nFrom: {user.full_name}\nUsername: {username}\nUser ID: `{user.id}`\n\nMessage:\n{update.message.text}"
    await context.bot.send_message(chat_id=ADMIN_ID, text=msg, parse_mode="Markdown")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & \~filters.COMMAND, handle_message))
    print("🤖 Grindpoint Bot is running...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
