import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
    filters,
    ContextTypes,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

GROUP_LINK = "https://t.me/+NJLTREq5F6E4NWE0"
REGISTER_LINK = "https://grindpoint.com.ng/register"

WITHDRAWAL_DATE, WITHDRAWAL_AMOUNT, WITHDRAWAL_EXTRA = range(3)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

WELCOME_TEXT = """Hello 👋

Welcome to *Grindpoint Support*!

I’m here to help you quickly.

What would you like to do?"""

HELP_MENU_TEXT = "Please choose what you need help with:"

def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("📢 Join Telegram Group", url=GROUP_LINK)],
        [InlineKeyboardButton("📝 Create Free Account", url=REGISTER_LINK)],
        [InlineKeyboardButton("🆘 I Need Help", callback_data="help_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)

def help_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("📋 How to Complete Tasks", callback_data="help_tasks")],
        [InlineKeyboardButton("💸 Withdrawal Problems", callback_data="help_withdrawal")],
        [InlineKeyboardButton("👤 Account / Login Issues", callback_data="help_account")],
        [InlineKeyboardButton("👥 Referral Questions", callback_data="help_referral")],
        [InlineKeyboardButton("❓ Other Problem (Talk to Human)", callback_data="help_human")],
        [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)

def back_to_help_keyboard():
    keyboard = [
        [InlineKeyboardButton("🔙 Back to Help Menu", callback_data="help_menu")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        WELCOME_TEXT,
        reply_markup=main_menu_keyboard(),
        parse_mode="Markdown"
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "main_menu":
        await query.edit_message_text(
            WELCOME_TEXT,
            reply_markup=main_menu_keyboard(),
            parse_mode="Markdown"
        )

    elif data == "help_menu":
        await query.edit_message_text(
            HELP_MENU_TEXT,
            reply_markup=help_menu_keyboard()
        )

    elif data == "help_tasks":
        text = """📋 *How to Complete Tasks Correctly*

Here’s the proper way to earn without problems:

1. Go to the *Tasks* or *View Ads (PTC)* page
2. Click on a task
3. Follow the instructions carefully
4. For PTC/Ads:
   - You must stay on the advertiser website for the full time
   - Do not switch tabs early or leave it idle
   - Do not use bots or scripts
5. After completing, claim your reward

⚠️ Important:
Using bots, auto-clickers, or staying idle can cancel your reward and may lead to account restriction.

Need more help? Go back to the menu."""
        await query.edit_message_text(text, reply_markup=back_to_help_keyboard(), parse_mode="Markdown")

    elif data == "help_account":
        text = """👤 *Account & Login Issues*

Common solutions:

• *Can’t login?*
  - Make sure you’re using the correct email
  - Try resetting your password
  - Clear browser cache or try another browser

• *Didn’t receive verification email?*
  - Check your spam/junk folder
  - Wait a few minutes and try again

• *Want to change your name or bank details?*
  - Name cannot be changed after registration (must match your bank account)
  - For bank details, contact support with your registered email

If your issue is still not solved, choose “Talk to Human”."""
        await query.edit_message_text(text, reply_markup=back_to_help_keyboard(), parse_mode="Markdown")

    elif data == "help_referral":
        text = """👥 *Referral Questions*

• You earn a bonus when someone registers with your link and completes their first task.
• Referral bonus depends on your tier:
  - Starter: ₦200
  - Hustler (10+ referrals): ₦300
  - Champion (50+ referrals): ₦500

• You can find your referral link on the Referral page after login.

• Referral bonus is usually credited automatically after the person completes their first valid task.

If your referral bonus has not entered after a long time, choose “Talk to Human” and give us the person’s email or username."""
        await query.edit_message_text(text, reply_markup=back_to_help_keyboard(), parse_mode="Markdown")

    elif data == "help_withdrawal":
        await query.edit_message_text(
            "💸 *Withdrawal Support*\n\n"
            "I need a few details so we can help you faster.\n\n"
            "First question:\n"
            "*When did you place the withdrawal?*\n"
            "(Example: Yesterday, 2 days ago, 28th October, etc.)",
            parse_mode="Markdown"
        )
        return WITHDRAWAL_DATE

    elif data == "help_human":
        await query.edit_message_text(
            "Okay. Please type your problem clearly.\n\n"
            "A human support agent will reply to you as soon as possible."
        )

async def withdrawal_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["withdrawal_date"] = update.message.text
    await update.message.reply_text(
        "Got it.\n\n"
        "Second question:\n"
        "*How much did you try to withdraw?*\n"
        "(Example: 1500, 3000, 5000)"
    )
    return WITHDRAWAL_AMOUNT

async def withdrawal_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["withdrawal_amount"] = update.message.text
    await update.message.reply_text(
        "Thank you.\n\n"
        "Last question (optional):\n"
        "Any extra information? (Transaction ID, error message, or just type 'None')"
    )
    return WITHDRAWAL_EXTRA

async def withdrawal_extra(update: Update, context: ContextTypes.DEFAULT_TYPE):
    extra = update.message.text
    user = update.effective_user

    date = context.user_data.get("withdrawal_date", "Not provided")
    amount = context.user_data.get("withdrawal_amount", "Not provided")

    username = f"@{user.username}" if user.username else "No username"
    text = (
        f"💸 *Withdrawal Support Request*\n\n"
        f"From: {user.full_name}\n"
        f"Username: {username}\n"
        f"User ID: `{user.id}`\n\n"
        f"• Date of withdrawal: {date}\n"
        f"• Amount: {amount}\n"
        f"• Extra info: {extra}"
    )
    await context.bot.send_message(chat_id=ADMIN_ID, text=text, parse_mode="Markdown")

    await update.message.reply_text(
        "✅ Thank you for the information.\n\n"
        "Your withdrawal issue has been sent to our support team.\n"
        "We will check and get back to you shortly.",
        reply_markup=main_menu_keyboard()
    )
    context.user_data.clear()
    return ConversationHandler.END

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message_text = update.message.text.strip().lower()

    if message_text in ["hi", "hello", "hey", "good morning", "good evening", "start", "help", "menu"]:
        await start(update, context)
        return

    username = f"@{user.username}" if user.username else "No username"
    text = (
        f"💬 *New Message from User*\n\n"
        f"From: {user.full_name}\n"
        f"Username: {username}\n"
        f"User ID: `{user.id}`\n\n"
        f"Message:\n{update.message.text}"
    )
    await context.bot.send_message(chat_id=ADMIN_ID, text=text, parse_mode="Markdown")

    await update.message.reply_text(
        "Thank you for your message.\n\n"
        "A human support agent will get back to you shortly.",
        reply_markup=main_menu_keyboard()
    )

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cancelled.", reply_markup=main_menu_keyboard())
    context.user_data.clear()
    return ConversationHandler.END

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    withdrawal_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_handler, pattern="^help_withdrawal$")],
        states={
            WITHDRAWAL_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, withdrawal_date)],
            WITHDRAWAL_AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, withdrawal_amount)],
            WITHDRAWAL_EXTRA: [MessageHandler(filters.TEXT & ~filters.COMMAND, withdrawal_extra)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(withdrawal_conv)
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Grindpoint Smart Support Bot is running...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
