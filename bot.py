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

GRUPPO_ID = -1004446298918



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "👋 Benvenuto!\n\n"
        "Invia foto, testo o file.\n"
        "Il contenuto verrà inviato automaticamente."
    )



async def inoltra(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        await context.bot.copy_message(
            chat_id=GRUPPO_ID,
            from_chat_id=update.message.chat.id,
            message_id=update.message.message_id
        )


        print(
            "MESSAGGIO COPIATO",
            flush=True
        )


    except Exception as e:

        print(
            "ERRORE:",
            e,
            flush=True
        )



def main():

    app = Application.builder().token(TOKEN).build()



    app.add_handler(
        CommandHandler(
            "start",
            start
        )
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

        data = request.get_json(force=True)


        update = Update.de_json(
            data,
            app.bot
        )


        loop = asyncio.new_event_loop()

        asyncio.set_event_loop(loop)


        loop.run_until_complete(
            app.process_update(update)
        )


        loop.close()


        return "ok"



    async def setup():

        await app.initialize()


        await app.bot.set_webhook(
            url="https://invio-candidature-bot.onrender.com/webhook"
        )


        await app.start()


        print(
            "BOT AVVIATO",
            flush=True
        )



    loop = asyncio.new_event_loop()

    asyncio.set_event_loop(loop)


    loop.run_until_complete(
        setup()
    )



    port = int(
        os.environ.get(
            "PORT",
            10000
        )
    )


    flask_app.run(
        host="0.0.0.0",
        port=port
    )



if __name__ == "__main__":
    main()
