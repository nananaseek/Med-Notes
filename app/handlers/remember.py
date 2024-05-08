from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext

from app.state.remember_state import RememberState

remember_router = Router()


@remember_router.callback_query(F.data == 'one in day', RememberState.remember)
async def remember(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(f'Виберіть час коли нагадувати')


@remember_router.callback_query(F.data == 'two in day', RememberState.remember)
async def remember(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(f'Виберіть години')


@remember_router.callback_query(F.data == 'period', RememberState.remember)
async def remember(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(f'Виберіть період нагадувань')
