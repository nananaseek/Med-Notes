import asyncio
import logging

from aiogram.enums import ContentType
from aiogram.types import CallbackQuery
from aiogram_dialog import BaseDialogManager, DialogManager
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.widgets.kbd import Button

from app.dialogs.states import ProgressSG, SearchDrugsSG
from app.parser.parser_service import parser_service
from app.redis.drug_cache import drug_cache


async def start_bg(
    callback: CallbackQuery,
    button: Button,
    manager: DialogManager,
):
    search_query = manager.dialog_data.get('drug_name')
    user_id = callback.from_user.id
    await manager.start(ProgressSG.progress)
    await asyncio.create_task(prepare_to_get_query(search_query, user_id, manager.bg()))


async def prepare_to_get_query(search_query: str, user_id: int, manager: BaseDialogManager):
    count = 13
    await drug_cache.save_user_query(search_query, user_id)
    data = await parser_service.get_search_drug_data(search_query)

    for item in data:
        if 'image' in item:
            item['image'] = MediaAttachment(ContentType.PHOTO, url=item['image'])

    for i in range(1, count + 1):
        await manager.update({
            "progress": i * 100 / count,
        })
    await manager.start(SearchDrugsSG.drug_card, data=data)


async def get_bg_data(dialog_manager: DialogManager, **kwargs):
    return {
        "progress": dialog_manager.dialog_data.get("progress", 0),
    }
