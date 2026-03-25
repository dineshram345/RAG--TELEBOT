import asyncio
import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import rag

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

HELP_TEXT = """Mini-RAG Bot

I answer questions using a local knowledge base about Python, Git, and Docker.

Commands:
/ask <question> - Ask me anything about the knowledge base
/help - Show this message

Example:
/ask What is a virtual environment?
/ask How do branches work in Git?
/ask What is Docker Compose?
"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_TEXT)


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_TEXT)


async def ask_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = " ".join(context.args) if context.args else ""
    if not question:
        await update.message.reply_text("Please provide a question. Example:\n/ask What is Docker?")
        return

    await update.message.reply_text("Searching...")

    try:
        answer = await asyncio.to_thread(rag.ask, question)
        await update.message.reply_text(answer)
    except Exception as e:
        logger.error(f"RAG error: {e}")
        await update.message.reply_text(f"Something went wrong: {e}")


async def text_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = (update.message.text or "").strip()
    if not question:
        return

    await update.message.reply_text("Searching...")
    try:
        answer = await asyncio.to_thread(rag.ask, question)
        await update.message.reply_text(answer)
    except Exception as e:
        logger.error(f"RAG error: {e}")
        await update.message.reply_text(f"Something went wrong: {e}")


def main():
    if not TOKEN:
        print("Error: Set TELEGRAM_BOT_TOKEN in your .env file")
        print("Get a token from @BotFather on Telegram")
        return

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("ask", ask_cmd))
    # Convenience: if user sends plain text (no leading '/'), answer it as the question.
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_msg))

    print("Bot is running... Press Ctrl+C to stop.")
    app.run_polling()


if __name__ == "__main__":
    main()
