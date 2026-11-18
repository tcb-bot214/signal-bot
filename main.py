import os
import threading
import asyncio
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.environ.get("BOT_TOKEN")
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Bot is working!")

async def signal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("SIGNAL Pair: USDJPY Action: BUY")

async def run_bot_async():
    print("=== BOT STARTING ===", flush=True)
    print("TOKEN EXISTS:", bool(TOKEN), flush=True)
    if not TOKEN:
        print("ERROR: BOT_TOKEN is missing!", flush=True)
        return
    try:
        app_bot = ApplicationBuilder().token(TOKEN).build()
        app_bot.add_handler(CommandHandler("start", start))
        app_bot.add_handler(CommandHandler("signal", signal))
        await app_bot.initialize()
        await app_bot.start()
        await app_bot.updater.start_polling()
        print("=== BOT POLLING STARTED ===", flush=True)
        await asyncio.Event().wait()
    except Exception as e:
        print("=== BOT CRASHED ===", flush=True)
        print(f"ERROR: {e}", flush=True)

def run_bot():
    asyncio.run(run_bot_async())

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
