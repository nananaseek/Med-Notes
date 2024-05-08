from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def start_keyboard():
    bt_search = KeyboardButton(text='Пошук препаратів')
    bt_user_menu = KeyboardButton(text='Меню користувача')

    kb = ReplyKeyboardMarkup(
        keyboard=[
            [bt_search, bt_user_menu]
        ],
        resize_keyboard=True
    )
    return kb
