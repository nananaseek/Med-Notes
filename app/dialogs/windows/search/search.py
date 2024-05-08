import operator

from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Group, Start, Select, Row, Cancel, Next, Back, Button, SwitchTo, Url, \
    SwitchInlineQuery, ScrollingGroup
from aiogram_dialog.widgets.media import DynamicMedia, StaticMedia
from aiogram_dialog.widgets.text import Const, Format, Progress, Multi

from app.dialogs.states import SearchDrugsSG
from app.dialogs.windows.processing.metods import start_bg
from app.dialogs.windows.search.methods import get_drag_search_data, handle_drug_name, get_handle_data, next_card, \
    previous_card, get_current_item, link_to_telegraph, get_telegraph_link, save_drug, remember_drug, get_time

GetDrugNameWin = Window(
    Const("Введіть назву ліків", when='Пошук препаратів'),
    Format('Ви ввели: {drug_name}', when='drug_name'),
    MessageInput(handle_drug_name),
    Row(
        Button(Const('шукати'), id='search_button', on_click=start_bg, when='drug_name')
    ),
    state=SearchDrugsSG.get_query,
    getter=get_handle_data
)

DrugCardWin = Window(
    DynamicMedia('image', when='image'),
    Multi(
        Format('{name}'),
        Format('{description}'),
        Format('Продається {prescriptionStatus}'),
        Format('Ціна: {price}'),
    ),
    Row(
        Button(Const('Зберегти'), id='save_drug', on_click=save_drug, when='save'),
        SwitchTo(
            Const('Нагадати'),
            id='remember_drug',
            state=SearchDrugsSG.when,
            when='remember'
        ),
    ),
    Row(
        SwitchTo(
            Const('Подивится опис в телеграмі'),
            id='drug_cart_telegram',
            state=SearchDrugsSG.drug_card_info
        ),
        Url(
            Const('Подивится опис на сайті'),
            Format('{url}'),
            id='drug_cart_site',
            when='url'
        ),
    ),
    Row(
        SwitchTo(
            Const("Назад"),
            id='previous_drug',
            state=SearchDrugsSG.drug_card,
            on_click=previous_card,
            when='not_first_card'
        ),
        Button(Format('{max_page}'), id='max_page_len', when='max_page'),
        SwitchTo(
            Const("Вперед"),
            id='next_drug',
            state=SearchDrugsSG.drug_card,
            on_click=next_card,
            when='not_last_card'
        ),
    ),
    state=SearchDrugsSG.drug_card,
    getter=get_drag_search_data
)


DrugInfoWin = Window(
    DynamicMedia('image', when='image'),
    Multi(
        Format('{name}'),
        Format('{description}'),
        Format('Продається {prescriptionStatus}'),
        Format('Ціна: {price}'),
    ),
    Group(
        Select(
            Format('{item[0]}'),
            id='telegraph_links',
            item_id_getter=operator.itemgetter(1),
            items='current_telegraph',
            on_click=link_to_telegraph
        ),
        width=1
    ),

    # Button(Const('Фармакологические свойства'), id='pharmacologicalProperties', on_click=link_to_telegraph),
    # Button(Const('Показания Эсцитам Асино'), id='indications', on_click=link_to_telegraph),
    # Button(Const('Применение Эсцитам Асино'), id='application', on_click=link_to_telegraph),
    # Button(Const('Противопоказания'), id='contraindications', on_click=link_to_telegraph),
    # Button(Const('Побочные эффекты'), id='sideEffects', on_click=link_to_telegraph),
    # Button(Const('Особые указания'), id='specificInstructions', on_click=link_to_telegraph),
    # Button(Const('Взаимодействия'), id='interactions', on_click=link_to_telegraph),
    # Button(Const('Передозировка'), id='overdosage', on_click=link_to_telegraph),
    # Button(Const('Условия хранения'), id='storingConditions', on_click=link_to_telegraph),
    Row(
        SwitchTo(
            Const('Назад до списку перепаратів'),
            id='back_to_search',
            state=SearchDrugsSG.drug_card
        ),
        Button(
            Const('Зберегти'),
            id='save_drug',
            on_click=save_drug
        )
    ),
    state=SearchDrugsSG.drug_card_info,
    getter=get_current_item
)

TelegraphLinkWin = Window(
    Format('{telegraph_link}'),
    Back(Const('Назад до карточки')),
    state=SearchDrugsSG.telegraph_link,
    getter=get_telegraph_link
)

RememberWin = Window(
    Const('Виберіть коли потрібно пити препарат'),
    ScrollingGroup(
        Select(
            Format('{item[0]}'),
            id='when',
            item_id_getter=operator.itemgetter(0),
            items='time',
            on_click=remember_drug
        ),
        id='time',
        width=4,
        height=4
    ),
    state=SearchDrugsSG.when,
    getter=get_time
)
