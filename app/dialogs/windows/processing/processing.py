from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Multi, Progress, Const

from app.dialogs.states import ProgressSG
from app.dialogs.windows.processing.metods import get_bg_data

bg_dialog = Window(
    Multi(
        Const("Your click is processing, please wait..."),
        Progress("progress", 10),
    ),
    state=ProgressSG.progress,
    getter=get_bg_data,
)

