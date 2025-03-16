import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Load environment variables
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 10000))
RENDER_URL = os.getenv("RENDER_URL")  # For webhook deployment

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

def main() -> None:
    """Starts the Telegram bot."""
    application = Application.builder().token(TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('content', content))
    application.add_handler(CommandHandler('chitti_video', chitti_video))
    application.add_handler(CommandHandler('kingfisher_video', kingfisher_video))
    application.add_handler(CommandHandler('amrutha_video', amrutha_video))

    # 🔹 Use Polling for Local Testing
    if os.getenv("MODE", "polling") == "polling":
        print("Bot is running in polling mode...")
        application.run_polling()
    else:
        # 🔹 Use Webhook for Deployment
        print(f"Bot is running in webhook mode on {RENDER_URL}")
        application.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=TOKEN,  
            webhook_url=f"{RENDER_URL}/{TOKEN}"
        )

if __name__ == '__main__':
    main()
