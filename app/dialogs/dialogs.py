import asyncio

from aiogram import Router, F
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram_dialog import Dialog, DialogManager, StartMode
from aiogram_dialog.api.exceptions import UnknownIntent

from app.database.services import user_services
from app.dialogs.states import RegistrationSG, MenuSG, SearchDrugsSG, UserMenuSG
from app.dialogs.windows.bot_info.bot_info import InfoMainWin
from app.dialogs.windows.menu.menu import LoginMainWin, UserMainWin, FavoriteDragWin, FavoriteCardWin
from app.dialogs.windows.processing.processing import bg_dialog
from app.dialogs.windows.registration.registration import RegMainWin, RegLoginWin
from app.dialogs.windows.search.search import GetDrugNameWin, DrugCardWin, DrugInfoWin, TelegraphLinkWin, RememberWin

from app.keyboards.default.start import start_keyboard
# from app.dialogs.windows.search.methods import prepare_to_get_query

dlg_router = Router()


@dlg_router.message(CommandStart())
async def handle_start_query(message: Message, dialog_manager: DialogManager):
    user_id = message.from_user.id
    if not await user_services.is_registered(user_id):
        await dialog_manager.start(RegistrationSG.main, mode=StartMode.RESET_STACK)
    else:
        await dialog_manager.start(MenuSG.main, mode=StartMode.RESET_STACK)


async def error_handler(event, dialog_manager: DialogManager):
    """Example of handling UnknownIntent Error and starting new dialog"""
    if isinstance(event.exception, UnknownIntent):
        await handle_start_query(event.update.callback_query, dialog_manager)
    else:
        return UNHANDLED


@dlg_router.message(Command('menu'))
async def handle_menu(message: Message):
    await message.answer('Клавіатура швидкого доступу відкрита!', reply_markup=start_keyboard())


@dlg_router.message(Command('search'))
@dlg_router.message(F.text == 'Пошук препаратів')
async def handle_search_query(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(SearchDrugsSG.get_query, mode=StartMode.RESET_STACK)


@dlg_router.message(F.text == 'Меню користувача')
async def handle_user_menu(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(UserMenuSG.main, mode=StartMode.RESET_STACK)


RegistrationDLG = Dialog(RegMainWin, RegLoginWin)
InfoDLG = Dialog(InfoMainWin)
MenuDLG = Dialog(LoginMainWin)
UserMenuDLG = Dialog(UserMainWin, FavoriteDragWin, FavoriteCardWin)
ProgressDLG = Dialog(bg_dialog)
SearchDLG = Dialog(GetDrugNameWin, DrugCardWin, DrugInfoWin, TelegraphLinkWin, RememberWin)

dlg_router.include_routers(
    RegistrationDLG,
    InfoDLG,
    MenuDLG,
    UserMenuDLG,
    SearchDLG,
    ProgressDLG
)
