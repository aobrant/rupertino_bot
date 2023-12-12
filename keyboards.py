from aiogram import types

kb_1 = [
        [types.KeyboardButton(text="Говорить")]
    ]
kb_2 = [
        [types.KeyboardButton(text="Писать")]
    ]
kb_img = [
         [types.KeyboardButton(text="img")]
]

keyboard_write = types.ReplyKeyboardMarkup(
    keyboard=kb_1,
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Введите запрос"
                                         )
keyboard_read = types.ReplyKeyboardMarkup(
    keyboard=kb_2,
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Введите запрос"
                                         )