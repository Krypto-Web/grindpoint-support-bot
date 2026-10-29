import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
    ConversationHandler, filters, ContextTypes,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

GROUP_LINK = "https://t.me/+NJLTREq5F6E4NWE0"
REGISTER_LINK = "https://grindpoint.com.ng/register"
LOGIN_LINK = "https://grindpoint.com.ng/login"
PTC_LINK = "https://grindpoint.com.ng/ptc"
DASHBOARD_LINK = "https://grindpoint.com.ng/dashboard"

# Conversation states for withdrawal
EMAIL, W_DATE, W_AMOUNT, W_BALANCE, W_EXTRA = range(5)

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# ====================== KEYBOARDS ======================

def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("📢 Join Telegram Group", url=GROUP_LINK)],
        [InlineKeyboardButton("📝 Create Free Account", url=REGISTER_LINK)],
        [InlineKeyboardButton("🔐 Login to Account", url=LOGIN_LINK)],
        [InlineKeyboardButton("⚡ Start Earning (PTC)", url=PTC_LINK)],
        [InlineKeyboardButton("🏠 Go to Dashboard", url=DASHBOARD_LINK)],
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

def back_keyboard():
    keyboard = [
        [InlineKeyboardButton("🔙 Back to Help Menu", callback_data="help_menu")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")],
    ]
    return InlineKeyboardMarkup(keyboard)

# ====================== MESSAGES ======================

WELCOME_TEXT = """Hello 👋

Welcome to *Grindpoint Support*!

I’m your official assistant. How can I help you today?"""

# ====================== HANDLERS ======================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_TEXT, reply_markup=main_menu_keyboard(), parse_mode="Markdown")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "main_menu":
        await query.edit_message_text(WELCOME_TEXT, reply_markup=main_menu_keyboard(), parse_mode="Markdown")

    elif data == "help_menu":
        await query.edit_message_text("Please choose what you need help with:", reply_markup=help_menu_keyboard())

    elif data == "help_tasks":
        text = """📋 *How to Complete Tasks Correctly*

Follow these steps carefully to avoid problems:

*For PTC / View Ads:*
1. Click “View Ad”
2. Read the warning carefully
3. Stay on the advertiser’s website for the full time shown
4. Do not switch tabs, minimise, or leave the page idle
5. After the time is complete, come back and click Claim

*Important Rules:*
• Using bots, scripts, or auto-clickers is strictly forbidden
• Staying idle or leaving early will cancel your reward
• Repeated abuse can lead to permanent ban and loss of balance

*Other Tasks (Surveys, Social, App installs):*
- Follow the exact instructions on each task
- Submit correct proof when required
- Do not use fake accounts or VPNs

Always complete tasks honestly so your account stays safe and you can keep earning."""
        await query.edit_message_text(text, reply_markup=back_keyboard(), parse_mode="Markdown")

    elif data == "help_account":
        text = """👤 *Account & Login Issues*

*Can’t log in?*
• Make sure you are using the correct email and password
• Try the “Forgot Password” option
• Clear your browser cache or try another browser / phone
• Make sure you have verified your email

*Didn’t receive verification email?*
• Check your Spam / Junk / Promotions folder
• Wait 5–10 minutes
• Try requesting the verification link again

*Name & Bank Details:*
• Your full name cannot be changed after registration (it must match your bank account)
• To update bank/wallet details, contact support with your registered email

*Account Restricted or Banned?*
If your account was restricted due to foul play (bots, multi-accounting, etc.), it may not be recoverable.

If you still need help, choose “Talk to Human”.
"""
        await query.edit_message_text(text, reply_markup=back_keyboard(), parse_mode="Markdown")

    elif data == "help_referral":
        text = """👥 *Referral Program*

You earn money when people join using your link and complete their first task.

*Referral Bonus Tiers:*
• Starter (0–9 referrals) → ₦200 per referral
• Hustler (10–49 referrals) → ₦300 per referral
• Champion (50+ referrals) → ₦500 per referral

*How it works:*
1. Copy your referral link from the Referral page
2. Share it with friends
3. When they register and complete their first valid task, you receive your bonus

*Bonus not showing?*
• Make sure the person used your exact link
• They must complete at least one valid task
• Wait a few hours after they finish the task
• If it still doesn’t appear, contact support with their email

Go to your Dashboard → Referral section to get your link.
"""
        await query.edit_message_text(text, reply_markup=back_keyboard(), parse_mode="Markdown")

    elif data == "help_withdrawal":
        await query.edit_message_text(
            "💸 *Withdrawal Support*\n\n"
            "To help you faster, I need some details.\n\n"
            "Please type your *registered email address* on Grindpoint:",
            parse_mode="Markdown"
        )
        return EMAIL

    elif data == "help_human":
        await query.edit_message_text(
            "Okay. Please type your problem clearly.\n\nA human support agent will reply as soon as possible."
        )

# ========== WITHDRAWAL CONVERSATION ==========

async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["email"] = update.message.text.strip()
    await update.message.reply_text(
        "Got it.\n\n"
        "When did you place the withdrawal?\n"
        "(Example: Yesterday, 2 days ago, 28th October)"
    )
    return W_DATE

async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["date"] = update.message.text.strip()
    await update.message.reply_text(
        "How much did you try to withdraw?\n"
        "(Example: 2000, 5000, 10000)"
    )
    return W_AMOUNT

async def get_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["amount"] = update.message.text.strip()
    await update.message.reply_text(
        "What is your *current balance* on Grindpoint right now?"
    )
    return W_BALANCE

async def get_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["balance"] = update.message.text.strip()
    await update.message.reply_text(
        "Any extra information?\n"
        "(Transaction reference, error message, or just type None)"
    )
    return W_EXTRA

async def get_extra(update: Update, context: ContextTypes.DEFAULT_TYPE):
    extra = update.message.text.strip()
    user = update.effective_user

    email = context.user_data.get("email", "Not provided")
    date = context.user_data.get("date", "Not provided")
    amount = context.user_data.get("amount", "Not provided")
    balance = context.user_data.get("balance", "Not provided")

    username = f"@{user.username}" if user.username else "No username"

    text = (
        f"💸 *New Withdrawal Support Request*\n\n"
        f"From: {user.full_name}\n"
        f"Username: {username}\n"
        f"Telegram ID: `{user.id}`\n\n"
        f"• Email: `{email}`\n"
        f"• Date of Withdrawal: {date}\n"
        f"• Amount: {amount}\n"
        f"• Current Balance: {balance}\n"
        f"• Extra Info: {extra}"
    )

    await context.bot.send_message(chat_id=ADMIN_ID, text=text, parse_mode="Markdown")

    await update.message.reply_text(
        "✅ Thank you. Your withdrawal details have been sent to the support team.\n\n"
        "We will check and get back to you shortly.",
        reply_markup=main_menu_keyboard()
    )
    context.user_data.clear()
    return ConversationHandler.END

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().lower()
    if text in ["hi", "hello", "hey", "good morning", "good evening", "start", "help", "menu"]:
        await start(update, context)
        return

    user = update.effective_user
    username = f"@{user.username}" if user.username else "No username"
    msg = (
        f"💬 *New Message*\n\n"
        f"From: {user.full_name}\n"
        f"Username: {username}\n"
        f"ID: `{user.id}`\n\n"
        f"Message:\n{update.message.text}"
    )
    await context.bot.send_message(chat_id=ADMIN_ID, text=msg, parse_mode="Markdown")
    await update.message.reply_text(
        "Thank you for your message. A human agent will reply shortly.",
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
            EMAIL: [MessageHandler(filters.TEXT & \~filters.COMMAND, get_email)],
            W_DATE: [MessageHandler(filters.TEXT & \~filters.COMMAND, get_date)],
            W_AMOUNT: [MessageHandler(filters.TEXT & \~filters.COMMAND, get_amount)],
            W_BALANCE: [MessageHandler(filters.TEXT & \~filters.COMMAND, get_balance)],
            W_EXTRA: [MessageHandler(filters.TEXT & \~filters.COMMAND, get_extra)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(withdrawal_conv)
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & \~filters.COMMAND, handle_message))

    print("🤖 Grindpoint Smart Support Bot is running...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
