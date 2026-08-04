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

print("VERSIONE BOT TEST 123")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "👋 Bot attivo!\n\n"
        "Invia un messaggio per il test."
    )


async def chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):

    print("========== UPDATE RICEVUTO ==========")
    print(update)
    print("=====================================")

    if update.effective_chat:
        print("CHAT ID:", update.effective_chat.id)
        print("TIPO:", update.effective_chat.type)



def main():

    app = Application.builder().token(TOKEN).build()


    app.add_handler(
        CommandHandler("start", start)
    )


    app.add_handler(
        MessageHandler(
            filters.ALL,
            chat_id
        )
    )


    flask_app = Flask(__name__)


    @flask_app.route("/")
    def home():
        return "Bot attivo"


    @flask_app.route("/webhook", methods=["POST"])
    def webhook():

        print("ARRIVATO WEBHOOK")

        data = request.get_json(force=True)

        print("========== DATI TELEGRAM ==========")
        print(data)
        print("===================================")


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

        print("BOT AVVIATO")



    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(setup())


    port = int(
        os.environ.get("PORT", 10000)
    )


    flask_app.run(
        host="0.0.0.0",
        port=port
    )



if __name__ == "__main__":
    main()
