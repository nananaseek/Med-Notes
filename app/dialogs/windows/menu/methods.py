import logging
from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button

from app.database.services import user_services, search_services
from app.dialogs.universal_methods import get_tg_id_from_manager
from app.parser.parser_service import parser_service


async def get_name(dialog_manager: DialogManager, **kwargs):
    tg_id = get_tg_id_from_manager(dialog_manager)
    user = await user_services.get_by_tg(tg_id)
    return {
        "name": user.name
    }


async def get_saved_drugs(dialog_manager: DialogManager, **kwargs):
    data = dialog_manager.dialog_data
    item_iterator = 1
    drugs_dict = {'not_first_page': True, 'not_last_page': True}
    if 'page_iterator' not in data:
        data.update(page_iterator=1)

    tg_id = get_tg_id_from_manager(dialog_manager)
    saved_drugs = await search_services.get_saved_drugs(
        user_id=tg_id,
        page=data['page_iterator'],
        object_per_page=4
    )

    if data['page_iterator'] > 1:
        drugs_dict['not_first_page'] = True
    else:
        drugs_dict.pop('not_first_page')

    if data['page_iterator'] * 4 < saved_drugs['objects_count']:
        drugs_dict['not_last_page'] = True
    else:
        drugs_dict.pop('not_last_page')

    drugs_dict['max_page'] = f'{data["page_iterator"]}/{saved_drugs['objects_count']}'

    for item in saved_drugs['pagination']:
        data[f'item_{item_iterator}'] = item.url
        drugs_dict[f'item_{item_iterator}'] = item.name
        data['name'] = item.name
        item_iterator += 1

    return drugs_dict


async def next_card(
        call: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    dialog_manager.dialog_data['page_iterator'] += 1


async def previous_card(
        call: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    dialog_manager.dialog_data['page_iterator'] -= 1


async def target_drug(
        call: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    dialog_manager.dialog_data['current_drug'] = call.data


async def get_drag_favorite_data(dialog_manager: DialogManager, **kwargs):
    data = dialog_manager.dialog_data
    concurrent_drug_url = data[f'{data['current_drug']}']
    try:
        drud_data = await parser_service.get_drug_page_data(concurrent_drug_url)
        telegraph_link = []
        iterator = 0
        drud_data.pop('page_id')
        for key, value in drud_data.items():
            telegraph_link.append((key, f'item_{iterator}', value))
            iterator += 1
        dialog_manager.dialog_data.update(current_telegraph=telegraph_link)
        data['current_telegraph'] = telegraph_link
    except AttributeError:
        dialog_manager.dialog_data.update(current_telegraph=None)
        data['current_telegraph'] = [('Препарат не має опису', 'Пусто', 'Пусто')]
    logging.info(data)
    return data
    # print(drud_data)


async def link_to_favorite_telegraph(
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
