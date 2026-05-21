import logging
import random
import re
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Основная часть (общая для всех ботов)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "8773077819:AAF1aot6JfRLiem5RX44-F4OisZems0SNPo"  # токен бота

RE_NUMBER = re.compile(r'^[+-]?\d+(?:[.,]\d+)?$')
RE_TWO_NUMBERS = re.compile(r'^\s*([+-]?\d+(?:[.,]\d+)?)\s*(?:[ ,;:]+)\s*([+-]?\d+(?:[.,]\d+)?)\s*$')

START_KEYBOARD = ReplyKeyboardMarkup([[KeyboardButton("старт")]], resize_keyboard=True)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот Рандомайзер.\n\n"
        "Функции:\n"
        "• Нажми кнопку 'старт' — покажу этот краткий туториал.\n"
        "• Введи одно число n — я верну случайное число от 0 до n.\n"
        "• Введи два числа в одной строке (через пробел, запятую, ; или :) — верну случайное число между ними.\n"
        "• Введи несколько строк (каждое значение с новой строки) — выберу одну строку случайно.\n",
        reply_markup=START_KEYBOARD
    )


# Функционал
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if text.lower() == "старт":
        await start_command(update, context)
        return

    m = RE_TWO_NUMBERS.match(text)
    if m:
        a_s, b_s = m.group(1), m.group(2)
        try:
            a = float(a_s.replace(',', '.'))
            b = float(b_s.replace(',', '.'))
        except ValueError:
            await update.message.reply_text("пожалуйста, введите корректные значения")
            return
        lo, hi = (a, b) if a <= b else (b, a)
        if float(lo).is_integer() and float(hi).is_integer():
            lo_i, hi_i = int(lo), int(hi)
            val = random.randint(lo_i, hi_i)
            await update.message.reply_text(str(val))
        else:
            val = random.uniform(lo, hi)
            await update.message.reply_text(str(val))
        return

    if RE_NUMBER.match(text):
        try:
            n = float(text.replace(',', '.'))
        except ValueError:
            await update.message.reply_text("пожалуйста, введите корректные значения")
            return
        if n.is_integer():
            n_i = int(n)
            if n_i >= 0:
                val = random.randint(0, n_i)
            else:
                val = random.randint(n_i, 0)
            await update.message.reply_text(str(val))
        else:
            if n >= 0:
                val = random.uniform(0, n)
            else:
                val = random.uniform(n, 0)
            await update.message.reply_text(str(val))
        return

    if '\n' in update.message.text:
        lines = [ln.strip() for ln in update.message.text.splitlines() if ln.strip()]
        if not lines:
            await update.message.reply_text("пожалуйста, введите корректные значения")
            return
        choice = random.choice(lines)
        await update.message.reply_text(choice)
        return

    if any(sep in text for sep in [',', ';']):
        parts = [p.strip() for p in re.split(r'[;,]', text) if p.strip()]
        if len(parts) >= 2:
            choice = random.choice(parts)
            await update.message.reply_text(choice)
            return

    await update.message.reply_text("пожалуйста, введите корректные значения")


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    logger.info("Бот запущен (long polling).")
    app.run_polling()


if __name__ == "__main__":
    main()
