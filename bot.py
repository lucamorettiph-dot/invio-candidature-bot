import os
import asyncio

from flask import Flask, request

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)


TOKEN = os.environ.get("BOT_TOKEN")

GRUPPO_ID = -1003951776949


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "👋 Benvenuto!\n\n"
        "Invia foto o messaggi.\n"
        "Il contenuto verrà inoltrato automaticamente."
    )


async def inoltra(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        # FOTO
        if update.message.photo:

            await context.bot.send_photo(
                chat_id=GRUPPO_ID,
                photo=update.message.photo[-1].file_id,
                caption=update.message.caption
            )


        # TESTO
        elif update.message.text:

            await context.bot.send_message(
                chat_id=GRUPPO_ID,
                text=update.message.text
            )


        # ALTRI TIPI DI MESSAGGIO
        else:

            await context.bot.forward_message(
                chat_id=GRUPPO_ID,
                from_chat_id=update.message.chat.id,
                message_id=update.message.message_id
            )


        await update.message.reply_text(
            "✅ Inviato correttamente"
        )


    except Exception as e:

        print("ERRORE INVIO:", e)



def main():

    app = Application.builder().token(TOKEN).build()


    app.add_handler(
        CommandHandler("start", start)
    )


    app.add_handler(
        MessageHandler(
            filters.ALL & ~filters.COMMAND,
            inoltra
        )
    )


    flask_app = Flask(__name__)


    @flask_app.route("/")
    def home():
        return "Bot attivo"


    @flask_app.route("/webhook", methods=["POST"])
    def webhook():

        update = Update.de_json(
            request.get_json(force=True),
            app.bot
        )

        asyncio.run(
            app.process_update(update)
        )

        return "ok"



    async def setup():

        await app.initialize()

        await app.bot.set_webhook(
            url="https://invio-candidature-bot.onrender.com/webhook"
        )

        await app.start()



    asyncio.run(setup())


    port = int(
        os.environ.get("PORT", 10000)
    )


    flask_app.run(
        host="0.0.0.0",
        port=port
    )



if __name__ == "__main__":
    main()
