from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Group, Next, Back, Start
from aiogram_dialog.widgets.text import Const, Format

from app.dialogs.states import RegistrationSG, InfoSG
from app.dialogs.windows.registration.methods import handle_name

RegMainWin = Window(
    Const("📎 Регестрация"),
    Group(
        Next(Const("Увійти")),
        Start(Const("Інформація про бота"), state=InfoSG.main, id="info"),
    ),
    state=RegistrationSG.main,
)

RegLoginWin = Window(
    Format("Введіть Ім'я:"),
    Group(Back(Const("Назад"))),
    MessageInput(handle_name),
    state=RegistrationSG.login,
)
