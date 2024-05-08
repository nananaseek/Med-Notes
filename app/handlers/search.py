from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from app.keyboards.inline.search import search_inline
from app.state.search_state import SearchState

search_router = Router()


@search_router.message(SearchState.search)
async def search_handler(message: types.Message, state: FSMContext):
    await state.set_state(SearchState.choice_item)
    await message.answer(
        f'Оберіть зі списку ваш препарат',
        reply_markup=search_inline()
    )


@search_router.callback_query(SearchState.choice_item)
async def callback_search_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(f'Ви вибрали цей препарат')
