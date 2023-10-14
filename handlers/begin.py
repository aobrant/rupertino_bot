import os

from aiogram import Router, types, F
import openai
from aiogram.filters import Command
from aiogram.fsm import state
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from dotenv import load_dotenv

from keyboards import keyboard_write, keyboard_read
from misc import help_message, States
from gtts import gTTS

router = Router()
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")

language='ru'


@router.message(Command("start"))
async def process_start_command(message: types.Message, state: FSMContext):
    await message.answer(" Hi! I'm Rupertino 👽 ", reply_markup=keyboard_write)
    await state.set_state(States.write_state)


@router.message(Command("help"))
async def process_help_command(message: types.Message):
    await message.answer(help_message)


@router.message(F.text.lower() == "говорить")
async def speak(message: types.Message, state=FSMContext):
    await message.answer(" Расскажу ", reply_markup=keyboard_read)
    await state.set_state(States.read_state)


@router.message(F.text.lower() == "писать")
async def speak(message: types.Message, state=FSMContext):
    await message.answer(" Напишу ", reply_markup=keyboard_write)
    await state.set_state(States.write_state)


@router.message(F.text)
async def message_response(message: types.Message, state: FSMContext):
    user_text = message.text
    gpt_response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=user_text,
        max_tokens=3000,
        api_key=openai_key
    )
    gpt_reply = gpt_response.choices[0].text
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
