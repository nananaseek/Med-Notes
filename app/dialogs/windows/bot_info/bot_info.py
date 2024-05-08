from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Group, Cancel
from aiogram_dialog.widgets.text import Const

from app.dialogs.states import InfoSG

InfoMainWin = Window(
    Const("Інформація про бота:\n"
          "Цей бот створений для того що б дізнаватися про медичні препарати та нагадування про прийом цих препаратів"
          "\n\nДля того щоб відкрити клавіатуру швидкого доступу напишіть команду /menu"),
    Group(Cancel(Const("Назад")),
          ),
    state=InfoSG.main,
)
