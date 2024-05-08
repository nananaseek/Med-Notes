from aiogram.utils.keyboard import InlineKeyboardBuilder


def search_inline():
    builder = InlineKeyboardBuilder()

    for index in range(1, 6):
        builder.button(text=f"Set {index}", callback_data=f"set:{index}")

    builder.adjust(1)

    return builder.as_markup()
