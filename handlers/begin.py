import os

from aiogram import Router, types, F
import openai
from aiogram.filters import Command
from dotenv import load_dotenv

from misc import help_message

router = Router()
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")


@router.message(Command("start"))
async def process_start_command(message: types.Message):
    await message.answer(
        "Hi! I'm Rupertino 👽 "
    )


@router.message(Command("help"))
async def process_help_command(message: types.Message):
    await message.answer(help_message)


@router.message(F.text)
async def message_response(message: types.Message):
    user_text = message.text
    gpt_response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=user_text,
        max_tokens=3000,
        api_key=openai_key
    )
    gpt_reply = gpt_response.choices[0].text
    await message.answer(gpt_reply)
