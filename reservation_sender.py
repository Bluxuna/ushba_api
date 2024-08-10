

from typing import final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN: final = "7369046862:AAFZfY9rd0Xrf6K6HDBTs788q8E3hBPV__M"
bot_username: final = '@Ushba_reservation_bot'

# telegram bot commands
async def start_command(update:Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text("გამარჯობა nifu uwu pruwpchkwkwkwk ")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("გამარჯობა უშბას ადმინო მითხარი რით შემიძლია დაგეხმარო ")


def handle_response(text: str)->str:
    if "ჯავშნები" in text:
        return " yvela javshani"

    return "i do not get"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    bot_username: final = '@Ushba_reservation_bot'
    print(f"user ({update.message.chat.id}) in {message_type}: {text}")

    response: str = handle_response(text)
    await update.message.reply_text(response)


app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler('start', start_command))
app.add_handler(CommandHandler('update', handle_message))
app.run_polling(poll_interval=5)
# send_email( 'hii', 'movida?','598311309@magti.com')
