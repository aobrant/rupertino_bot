import asyncio
import logging

import openai
from pydub import AudioSegment
from aiogram import Bot, Dispatcher, types
import os
from dotenv import load_dotenv
from aiogram import F

openai_key = os.getenv("OPENAI_API_KEY")

from handlers import begin, vision, audio_resp
from misc import help_message, recognise

load_dotenv()
TelegramToken = os.getenv("TOKEN")
openai_key = os.getenv("OPENAI_API_KEY")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TelegramToken)
dp = Dispatcher()

dp.include_router(vision.router)
dp.include_router(audio_resp.router)
dp.include_router(begin.router)


@dp.message(F.voice)
async def converting_audio(message: types.Message):
    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    current_directory = os.getcwd()
    audio_directory = os.path.join(current_directory, "AUDIO/")
    if not os.path.exists(audio_directory):
        os.makedirs(audio_directory)
    audio_path = audio_directory + "audio.ogg"
    audio_path_full_converted = audio_directory + "audio.wav"
    await bot.download_file(file_path, audio_path)
    os.system("ffmpeg -i " + audio_path + "  " + audio_path_full_converted)
    text = recognise(audio_path_full_converted)
    os.remove(audio_path)
    os.remove(audio_path_full_converted)
    gpt_response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=text,
        max_tokens=3000,
        api_key=openai_key
    )
    gpt_reply = gpt_response.choices[0].text
    await message.answer(gpt_reply)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
