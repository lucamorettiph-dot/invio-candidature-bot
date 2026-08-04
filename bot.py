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
        "Invia foto, video, file o messaggi.\n"
        "Il contenuto verrà inviato automaticamente."
    )



async def inoltra(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        messaggio = update.message


        # FOTO
        if messaggio.photo:

            await context.bot.send_photo(
                chat_id=GRUPPO_ID,
                photo=messaggio.photo[-1].file_id,
                caption=messaggio.caption
            )


        # VIDEO
        elif messaggio.video:

            await context.bot.send_video(
                chat_id=GRUPPO_ID,
                video=messaggio.video.file_id,
                caption=messaggio.caption
            )


        # DOCUMENTI / FILE
        elif messaggio.document:

            await context.bot.send_document(
                chat_id=GRUPPO_ID,
                document=messaggio.document.file_id,
                caption=messaggio.caption
            )


        # AUDIO
        elif messaggio.audio:

            await context.bot.send_audio(
                chat_id=GRUPPO_ID,
                audio=messaggio.audio.file_id,
                caption=messaggio.caption
            )


        # TESTO
        elif messaggio.text:

            await context.bot.send_message(
                chat_id=GRUPPO_ID,
                text=messaggio.text
            )


        else:

            print(
                "Messaggio non supportato",
                flush=True
            )


        print(
            "MESSAGGIO INVIATO AL GRUPPO",
            flush=True
        )


    except Exception as e:

        print(
            "ERRORE INVIO:",
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
