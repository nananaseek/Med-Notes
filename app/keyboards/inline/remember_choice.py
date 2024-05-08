from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def remember_choice_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Раз на день', callback_data='one in day')
            ],
            [
                InlineKeyboardButton(text='Декілька раз на день', callback_data='two in day')
            ],
            [
                InlineKeyboardButton(text='Періодично', callback_data='period')
            ]
        ]
    )
