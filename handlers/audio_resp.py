
from aiogram import Router, types, F
import speech_recognition as sr
from gtts import gTTS



router = Router()
language='ru_RU'
r = sr.Recognizer()

def talk_audio(text, language='ru'):
    my_audio = gTTS(text=text, lang=language, slow=False)





