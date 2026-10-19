import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
import os
import io
import contextlib
from pathlib import Path
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from organizer import get_category, organize, undo

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ALLOWED = int(os.getenv("ALLOWED_USER_ID", "0"))
DOWNLOADS = Path.home() / "Downloads"


def allowed(update: Update) -> bool:
    return update.effective_user.id == ALLOWED


async def myid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Your ID: {update.effective_user.id}")


async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not allowed(update):
        return
    counts = {}
    for f in DOWNLOADS.iterdir():
        if f.is_file():
            c = get_category(f)
            counts[c] = counts.get(c, 0) + 1
    text = "\n".join(f"{k}: {v}" for k, v in counts.items())
    await update.message.reply_text(text or "Nothing to organize")


async def run(update: Update, dry_run: bool):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        organize(DOWNLOADS, dry_run=dry_run)
    await update.message.reply_text(buf.getvalue()[:4000] or "Nothing to do")


async def preview(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if allowed(update):
        await run(update, True)


async def organize_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if allowed(update):
        await run(update, False)


async def undo_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not allowed(update):
        return
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        undo()
    await update.message.reply_text(buf.getvalue()[:4000] or "Nothing to undo")


PROXY = "socks5://127.0.0.1:10808"
app = (
    ApplicationBuilder()
    .token(TOKEN)
    .proxy(PROXY)
    .get_updates_proxy(PROXY)
    .connect_timeout(30)
    .read_timeout(30)
    .write_timeout(30)
    .pool_timeout(30)
    .get_updates_connect_timeout(30)
    .get_updates_read_timeout(30)
    .get_updates_write_timeout(30)
    .get_updates_pool_timeout(30)
    .build()
)

app.add_handler(CommandHandler("myid", myid))
app.add_handler(CommandHandler("report", report))
app.add_handler(CommandHandler("preview", preview))
app.add_handler(CommandHandler("organize", organize_cmd))
app.add_handler(CommandHandler("undo", undo_cmd))
app.run_polling(bootstrap_retries=-1)