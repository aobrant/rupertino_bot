from aiogram.utils.markdown import text
import speech_recognition as sr
from aiogram.fsm.state import StatesGroup, State

help_message = text(
    "/start",
    "/help",
    "begining with @ picture",
    sep="\n"
)

r = sr.Recognizer()
language = 'ru_RU'


def recognise(filename):
    with sr.AudioFile(filename) as source:
        audio_text = r.listen(source)
        try:
            text_r = r.recognize_google(audio_text, language=language)
            return text_r
        except:
            print('Sorry.. run again...')
            return "Sorry.. run again..."


class States(StatesGroup):
    write_state = State()
    read_state = State()

