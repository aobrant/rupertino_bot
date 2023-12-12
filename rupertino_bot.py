import asyncio
import logging

import openai
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from gtts import gTTS
from aiogram import Bot, Dispatcher, types
import os
from dotenv import load_dotenv
from aiogram import F
from openai import AsyncOpenAI

from misc import States

openai_key = os.getenv("OPENAI_API_KEY")

from handlers import begin, vision, audio_resp
from misc import help_message, recognise

language = 'ru'

load_dotenv()
TelegramToken = os.getenv("TOKEN")
openai_key = os.getenv("OPENAI_API_KEY")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TelegramToken)
dp = Dispatcher()

dp.include_router(vision.router)
dp.include_router(audio_resp.router)
dp.include_router(begin.router)

client = AsyncOpenAI(
    api_key=openai_key
)


@dp.message(F.voice)
async def converting_audio(message: types.Message, state: FSMContext):
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
    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": text,
            }
        ],
        # model="gpt-3.5-turbo",
        model="gpt-4-1106-preview",
    )
    gpt_reply = chat_completion.choices[0].message.content
    current_state = await state.get_state()
    if current_state == States.write_state:
        await message.answer(gpt_reply)
    elif current_state == States.read_state:
        my_audio = gTTS(text=gpt_reply, lang=language, slow=False)
        current_directory = os.path.dirname(os.path.abspath(__file__))
        aud_folder_path = os.path.join(current_directory, 'AUDIO')
        if not os.path.exists(aud_folder_path):
            os.makedirs(aud_folder_path)
        user_id = message.from_user.id
        name1 = str(user_id)
        name2 = 'mp3'
        name = '.'.join([name1, name2])
        file_path = os.path.join(aud_folder_path, name)
        my_audio.save(file_path)
        cat = FSInputFile(file_path)
        await message.answer_voice(cat)
        try:
            os.remove(file_path)
        except FileNotFoundError:
            print(f"Файл {file_path} не найден.")
        except Exception as e:
            print(f"Произошла ошибка при удалении файла: {str(e)}")

    else:
        await message.answer(gpt_reply)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
