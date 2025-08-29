# main.py
from flask import Flask
import threading
from telegram.ext import Updater, CommandHandler
import os

# --- Telegram Bot Code ---
TOKEN = os.getenv("BOT_TOKEN")   # Read token from Render Environment Variables

def start(update, context):
    update.message.reply_text("Hello! I'm alive on Render 🚀")

def run_bot():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()

# --- Flask App (for Render health check) ---
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running on Render!"

# --- Run both Flask + Bot ---
if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))