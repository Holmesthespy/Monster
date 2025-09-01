#!/usr/bin/env python3
# HelinaBot - Rose-like lightweight version

import logging
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatPermissions
)
from telegram.ext import (
    Updater, CommandHandler, CallbackQueryHandler,
    MessageHandler, Filters, CallbackContext
)

# --- BOT TOKEN ---
BOT_TOKEN = "8491430292:AAFoHzc8cVF3hXZyxhxd3H0-MkamChi6cX8"

# --- LINKS (change to your real ones) ---
OUR_CHANNELS_LINK = "https://t.me/YourChannelLink"
CONTENT_LINK = "https://t.me/YourContentLink"

# --- Logging ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- Helper: Admin check ---
def is_admin(update: Update, context: CallbackContext) -> bool:
    try:
        user_id = update.effective_user.id
        chat = update.effective_chat
        member = chat.get_member(user_id)
        return member.status in ["administrator", "creator"]
    except Exception:
        return False

# --- START Command ---
def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("📢 Our Channels", url=OUR_CHANNELS_LINK)],
        [InlineKeyboardButton("📚 Content", url=CONTENT_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "🤖 Welcome to Helina Bot!\nChoose an option below:",
        reply_markup=reply_markup
    )

# --- Greeting New Members ---
def greet_new_member(update: Update, context: CallbackContext):
    for member in update.message.new_chat_members:
        update.message.reply_text(
            f"👋 Welcome {member.mention_html()}! Enjoy your stay 🎉",
            parse_mode="HTML"
        )

# --- BAN Command ---
def ban(update: Update, context: CallbackContext):
    if not is_admin(update, context):
        update.message.reply_text("❌ Only admins can use this command.")
        return
    if not update.message.reply_to_message:
        update.message.reply_text("Reply to a user to ban them.")
        return
    user = update.message.reply_to_message.from_user
    try:
        context.bot.kick_chat_member(update.effective_chat.id, user.id)
        update.message.reply_text(f"🚫 Banned {user.first_name}")
    except Exception as e:
        update.message.reply_text("Failed to ban user: " + str(e))

# --- MUTE Command ---
def mute(update: Update, context: CallbackContext):
    if not is_admin(update, context):
        update.message.reply_text("❌ Only admins can use this command.")
        return
    if not update.message.reply_to_message:
        update.message.reply_text("Reply to a user to mute them.")
        return
    user = update.message.reply_to_message.from_user
    try:
        context.bot.restrict_chat_member(
            update.effective_chat.id,
            user.id,
            ChatPermissions(can_send_messages=False)
        )
        update.message.reply_text(f"🔇 Muted {user.first_name}")
    except Exception as e:
        update.message.reply_text("Failed to mute user: " + str(e))

# --- UNMUTE Command ---
def unmute(update: Update, context: CallbackContext):
    if not is_admin(update, context):
        update.message.reply_text("❌ Only admins can use this command.")
        return
    if not update.message.reply_to_message:
        update.message.reply_text("Reply to a user to unmute them.")
        return
    user = update.message.reply_to_message.from_user
    try:
        context.bot.restrict_chat_member(
            update.effective_chat.id,
            user.id,
            ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        )
        update.message.reply_text(f"🔊 Unmuted {user.first_name}")
    except Exception as e:
        update.message.reply_text("Failed to unmute user: " + str(e))

# --- PURGE Command ---
def purge(update: Update, context: CallbackContext):
    if not is_admin(update, context):
        update.message.reply_text("❌ Only admins can use this command.")
        return
    if not update.message.reply_to_message:
        update.message.reply_text("Reply to a message to start purging.")
        return

    chat = update.effective_chat
    message_id_start = update.message.reply_to_message.message_id
    message_id_end = update.message.message_id

    try:
        for msg_id in range(message_id_start, message_id_end + 1):
            context.bot.delete_message(chat.id, msg_id)
        confirmation = update.message.reply_text("✅ Messages purged.")
        context.job_queue.run_once(lambda ctx: confirmation.delete(), 3)
    except Exception as e:
        update.message.reply_text("Failed to purge messages: " + str(e))

# --- MAIN ---
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ban", ban))
    dp.add_handler(CommandHandler("mute", mute))
    dp.add_handler(CommandHandler("unmute", unmute))
    dp.add_handler(CommandHandler("purge", purge))

    # Greetings
    dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, greet_new_member))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()