import os
import asyncio

from flask import Flask, request

from telegram import Update, InputMediaPhoto

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
        "Invia foto, messaggi o file.\n"
        "Il contenuto verrà inoltrato automaticamente."
    )



async def inoltra(update: Update, context: ContextTypes.DEFAULT_TYPE):

    try:

        msg = update.message


        # ALBUM DI FOTO
        if msg.media_group_id:

            if "album" not in context.chat_data:
                context.chat_data["album"] = []

            context.chat_data["album"].append(
                msg.photo[-1].file_id
            )


            await asyncio.sleep(2)


            media = []

            for foto in context.chat_data["album"]:

                media.append(
                    InputMediaPhoto(
                        media=foto
                    )
                )


            await context.bot.send_media_group(
                chat_id=GRUPPO_ID,
                media=media
            )


            context.chat_data["album"] = []



        # FOTO SINGOLA
        elif msg.photo:

            await context.bot.send_photo(
                chat_id=GRUPPO_ID,
                photo=msg.photo[-1].file_id,
                caption=msg.caption
            )



        # TESTO
        elif msg.text:

            await context.bot.send_message(
                chat_id=GRUPPO_ID,
                text=msg.text
            )



        # DOCUMENTI / FILE

        elif msg.document:

            await context.bot.send_document(
                chat_id=GRUPPO_ID,
                document=msg.document.file_id,
                caption=msg.caption
            )



        # VIDEO

        elif msg.video:

            await context.bot.send_video(
                chat_id=GRUPPO_ID,
                video=msg.video.file_id,
                caption=msg.caption
            )


        print("MESSAGGIO INVIATO", flush=True)


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
