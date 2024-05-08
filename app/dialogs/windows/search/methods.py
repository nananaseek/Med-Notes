import asyncio
import logging
from typing import Any

from aiogram.enums import ContentType
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, BaseDialogManager, DialogProtocol, ShowMode
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const
from apscheduler.schedulers.background import BackgroundScheduler

from app.database.schemas import create_user_search
from app.database.services import user_services, search_services
from app.dialogs.states import ProgressSG
from app.dialogs.universal_methods import get_tg_id_from_manager
from app.parser.parser_service import parser_service
from app.redis.drug_cache import drug_cache


async def handle_drug_name(message: Message, dialog: DialogProtocol, manager: DialogManager):
    manager.show_mode = ShowMode.EDIT
    manager.dialog_data["drug_name"] = 'есцетам'#message.text
    await message.delete()


async def get_handle_data(dialog_manager: DialogManager, **kwargs):
    if 'drug_name' in dialog_manager.dialog_data:
        return {'drug_name': dialog_manager.dialog_data['drug_name']}
    else:
        return {'Пошук препаратів': 'Пошук препаратів'}


async def dell_message(call: CallbackQuery, button: Button, dialog: DialogManager):
    await call.message.delete()


async def get_drag_search_data(dialog_manager: DialogManager, **kwargs):
    # await drug_cache.get_user_query()
    # parser_service.get_search_drug_data()
    data = dialog_manager.start_data

    if 'iterator' in dialog_manager.dialog_data:
        iterator = dialog_manager.dialog_data.get('iterator')
    else:
        dialog_manager.dialog_data['iterator'] = 0
        iterator = 0

    drug: dict = data[int(iterator)]
    dialog_manager.dialog_data.update(current_drug=drug)

    if 'dict_len' not in dialog_manager.dialog_data:
        dialog_manager.dialog_data.update(dict_len=len(drug))
        dict_len = len(drug)
    else:
        dict_len = int(dialog_manager.dialog_data['dict_len'])

    if iterator == 0:
        if 'not_first_card' in drug:
            drug.pop('not_first_card')
    else:
        drug.update(not_first_card=True)

    if 'not_last_card' not in drug:
        drug.update(not_last_card=True)
    if iterator == dict_len:
        drug.pop('not_last_card')

    drug['max_page'] = f'{iterator + 1}/{dict_len + 1}'

    drag_url = await search_services.is_saved_url(drug['url'])
    drug['save'] = True
    if drag_url:
        drug.pop('save')
        drug['remember'] = True

    return drug


async def get_time(dialog_manager: DialogManager, **kwargs):
    data = dialog_manager.dialog_data['current_drug']
    remember_time = [(f'{t}:00', f'{t}', f'{data['name']}') for t in range(0, 24)]
    dialog_manager.dialog_data['remember_time'] = remember_time
    return {
        'time': remember_time
    }


async def remember_drug(
        call: CallbackQuery,
        widget: Any,
        manager: DialogManager,
        item_id: str
):
    data = manager.dialog_data['remember_time']
    data_time = item_id

    for set_data in data:
        if data_time in set_data:
            remember_call = set_data[2]
            t_name = set_data[1]
            break
        else:
            t_name = 'None'

    async def remember():
        await call.message.answer(f'Час випити {remember_call}')

    scheduler = BackgroundScheduler()
    scheduler.add_job(remember, 'cron', hour=t_name, minute=0)
    scheduler.start()
    await call.answer('Нагадування встановлено')


async def next_card(
        call: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    dialog_manager.dialog_data['iterator'] += 1


async def previous_card(
        call: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    dialog_manager.dialog_data['iterator'] -= 1


async def get_current_item(dialog_manager: DialogManager, **kwargs):
    data = dialog_manager.dialog_data.get('current_drug')
    try:
        current_drug_page = await parser_service.get_drug_page_data(data['url'])
        telegraph_link = []
        iterator = 0
        current_drug_page.pop('page_id')
        for key, value in current_drug_page.items():
            telegraph_link.append((key, f'item_{iterator}', value))
            iterator += 1
        dialog_manager.dialog_data.update(current_telegraph=telegraph_link)
        data['current_telegraph'] = telegraph_link
    except AttributeError:
        dialog_manager.dialog_data.update(current_telegraph=None)
        data['current_telegraph'] = [('Препарат не має опису', 'Пусто', 'Пусто')]
    logging.info(data)
    return data


async def link_to_telegraph(
        call: CallbackQuery,
        widget: Any,
        manager: DialogManager,
        item_id: str
):
    data = manager.dialog_data['current_telegraph']
    if data is None:
        await call.answer('Препарат не має опису')
    for item in data:
        if item_id in item:
            manager.dialog_data.update(telegraph_link=f'{item[2]}')
            await manager.next()


async def get_telegraph_link(dialog_manager: DialogManager, **kwargs):
    return {'telegraph_link': dialog_manager.dialog_data['telegraph_link']}


async def save_drug(
        call: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    data = dialog_manager.dialog_data.get('current_drug')
    create_schema = create_user_search(
        url=data['url'],
        name=data['name'],
        search_query=data['search_query']
    )
    await search_services.create(
        schema=create_schema,
        user_id=call.from_user.id
    )
    await call.answer('Ліки збережені')

