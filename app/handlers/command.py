from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from app.keyboards.inline.remember_choice import remember_choice_menu
from app.state.remember_state import RememberState
from app.state.search_state import SearchState
from app.keyboards.inline.search import search_inline

command_router = Router()


@command_router.message(CommandStart())
async def start(message: types.Message):
    await message.answer(f'''Доброго дня {message.from_user.username} ось доступні команди:
    /search
    /remember
    /favorite
    /history
    ''')


@command_router.message(Command('search'))
async def search(message: types.Message, state: FSMContext):
    await message.answer(f'Напишіть назву препарату')
    await state.set_state(SearchState.search)


@command_router.message(Command('favorite'))
async def favorite(message: types.Message):
    await message.answer(f'Список ваших збережених препаратів', reply_markup=search_inline())


@command_router.message(Command('remember'))
async def remember(message: types.Message, state: FSMContext):
    await message.answer(
        f'З якою періодичністю потрібно нагадувати про препарат',
        reply_markup=await remember_choice_menu()
    )
    await state.set_state(RememberState.remember)


@command_router.message(Command('history'))
async def history(message: types.Message):
    await message.answer(f'Історія пошуку', reply_markup=search_inline())
