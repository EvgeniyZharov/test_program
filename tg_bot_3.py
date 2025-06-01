import os
import uuid
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from file_1 import denoise_audio  # твоя функция из file_1.py
from pydub import AudioSegment

BOT_TOKEN = '7608054784:AAGxhdCSrqvcpz4OEBAUdwdSxRvyUNSSmWY'

MAX_SIZE_MB = 50

def get_file_size(path):
    return os.path.getsize(path) / (1024 * 1024)

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    if not document:
        await update.message.reply_text("Пожалуйста, отправь аудиофайл как *документ*, до 50 МБ.")
        return

    if document.file_size > MAX_SIZE_MB * 1024 * 1024:
        await update.message.reply_text("Файл превышает 20 МБ — Telegram не поддерживает такую передачу.")
        return

    uid = str(uuid.uuid4())
    original_file = f"{uid}_{document.file_name}"
    converted_wav = f"{uid}_converted.wav"
    processed_wav = f"{uid}_processed.wav"

    try:
        file = await context.bot.get_file(document.file_id)
        await file.download_to_drive(original_file)

        # Конвертация в WAV (если не WAV)
        os.system(f'ffmpeg -i "{original_file}" -ar 16000 -ac 1 "{converted_wav}" -y')

        # Обработка
        denoise_audio(converted_wav, processed_wav)

        # Отправка пользователю
        await update.message.reply_text("✅ Обработка завершена. Вот улучшенное аудио:")
        await update.message.reply_audio(audio=open(processed_wav, 'rb'))

    except Exception as e:
        await update.message.reply_text("Произошла ошибка при обработке аудиофайла.")
        print("Ошибка:", e)

    # Очистка
    for f in [original_file, converted_wav, processed_wav]:
        if os.path.exists(f):
            os.remove(f)

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.Document.AUDIO, handle_audio))
    print("Бот запущен. Ждёт аудиофайлы до 50 МБ...")
    app.run_polling()
