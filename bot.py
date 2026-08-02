import os
from telegram import Update, InputMediaPhoto
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = os.environ.get("BOT_TOKEN")

GRUPPO_ID = -1003951776949

# memoria temporanea delle candidature
candidature = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat.id

    candidature[user_id] = {
        "foto": [],
        "dati": None
    }

    await update.message.reply_text(
        "👋 Benvenuto!\n\n"
        "Invia da 5 a 10 foto della candidata.\n"
        "Dopo le foto invia nome ed età."
    )


async def ricevi_foto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat.id

    if user_id not in candidature:
        candidature[user_id] = {
            "foto": [],
            "dati": None
        }

    foto = update.message.photo[-1].file_id

    candidature[user_id]["foto"].append(foto)

    numero = len(candidature[user_id]["foto"])

    await update.message.reply_text(
        f"📸 Foto ricevuta ({numero}/10)\n"
        "Puoi inviarne altre oppure scrivere nome ed età."
    )


async def ricevi_testo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.chat.id

    testo = update.message.text

    if user_id not in candidature:
        return

    candidature[user_id]["dati"] = testo

    foto = candidature[user_id]["foto"]

    if len(foto) < 5:
        await update.message.reply_text(
            "⚠️ Servono almeno 5 foto prima di inviare la candidatura."
        )
        return

    await context.bot.send_message(
        chat_id=GRUPPO_ID,
        text=f"📸 NUOVA CANDIDATURA\n\n📝 Dati:\n{testo}"
    )

    media = []

    for f in foto:
        media.append(
            InputMediaPhoto(media=f)
        )

    await context.bot.send_media_group(
        chat_id=GRUPPO_ID,
        media=media
    )

    await update.message.reply_text(
        "✅ Candidatura inviata correttamente!"
    )

    del candidature[user_id]


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(filters.PHOTO, ricevi_foto)
    )

    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, ricevi_testo)
    )

    print("Bot avviato")

    import asyncio

    async def run():
        await app.initialize()
        await app.start()
        await app.updater.start_polling()

        await asyncio.Event().wait()

    asyncio.run(run())


if __name__ == "__main__":
    main()
