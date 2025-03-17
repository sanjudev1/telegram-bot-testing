import os
import asyncio
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask, request, jsonify

# Load environment variables
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 8000))
RENDER_URL = os.getenv("RENDER_URL")  # Webhook URL from Render
MODE = os.getenv("MODE", "polling")

if not TOKEN:
    raise ValueError("BOT_TOKEN environment variable is missing!")

# Initialize Flask App & Telegram Bot Application
app = Flask(__name__)
application = Application.builder().token(TOKEN).build()

# Define bot commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a welcome message with available commands."""
    await update.message.reply_text(
        "🎬 Welcome to the Film Making Department 🎬\n\n"
        "/help  - Contact my team for more info\n"
        "/content - View sample direction styles\n"
        "/contact - Reach out to my team 📞 9542862232\n"
        "/chitti_video - Chitti cover song 🎶\n"
        "/kingfisher_video - Kingfisher short film 🎥\n"
        "/amrutha_video - Amrutha cover song 🎵"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends help information."""
    await update.message.reply_text(
        "💡 **Help Center** 💡\n\n"
        "/start - Restart the bot\n"
        "/content - View amazing direction styles\n"
        "/contact - 📞 Call my team at 9542862232\n"
        "/chitti_video - Chitti cover song 🎶\n"
        "/kingfisher_video - Kingfisher short film 🎥\n"
        "/amrutha_video - Amrutha cover song 🎵"
    )

async def content(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends YouTube link for film content."""
    await update.message.reply_text("🎥 Check out our playlists: https://www.youtube.com/@localtouringtalkiesltt4999")

async def chitti_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends the Chitti cover song link."""
    await update.message.reply_text("🎶 Chitti Cover Song: https://www.youtube.com/watch?v=ro77dYAYmGM")

async def kingfisher_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends the Kingfisher short film link."""
    await update.message.reply_text("🎬 Kingfisher Short Film: https://www.youtube.com/watch?v=6N10zpHvS9I")

async def amrutha_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends the Amrutha cover song link."""
    await update.message.reply_text("🎵 Amrutha Cover Song: https://www.youtube.com/watch?v=lIo46bYftZE")

# Register command handlers
application.add_handler(CommandHandler('start', start))
application.add_handler(CommandHandler('help', help_command))
application.add_handler(CommandHandler('content', content))
application.add_handler(CommandHandler('chitti_video', chitti_video))
application.add_handler(CommandHandler('kingfisher_video', kingfisher_video))
application.add_handler(CommandHandler('amrutha_video', amrutha_video))

# Webhook Update Handler
async def webhook_update():
    """Receives updates from Telegram Webhook."""
    update_data = request.get_json()
    asyncio.run(webhook_update(update_data))  # Ensures proper async execution
    return jsonify({"status": "OK"}), 200

# Flask Routes
@app.route("/", methods=["GET"])
def health_check():
    """Health check endpoint to verify the server is running."""
    return jsonify({"status": "Bot is running!"}), 200

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    """Receives updates from Telegram Webhook."""
    update_data = request.get_json()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(webhook_update(update_data))

    return jsonify({"status": "OK"}), 200

# Fix: Assign the Flask app as a WSGI application callable for Gunicorn
get_app = app

if __name__ == "__main__":
    print(f"Starting bot in {MODE} mode on port {PORT}...")

    if MODE == "polling":
        print("Bot is running in polling mode...")
        application.run_polling()
    else:
        print(f"Bot is running in webhook mode on {RENDER_URL}")
        asyncio.run(application.bot.setWebhook(f"{RENDER_URL}/{TOKEN}"))
        app.run(host="0.0.0.0", port=PORT)
