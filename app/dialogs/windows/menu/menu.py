import operator

from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Group, Start, Select, Button, Row, SwitchTo, Back, Url
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format, Multi

from app.dialogs.states import InfoSG, MenuSG, UserMenuSG
from app.dialogs.windows.menu.methods import get_name, get_saved_drugs, previous_card, next_card, \
    get_drag_favorite_data, target_drug, link_to_favorite_telegraph

LoginMainWin = Window(
    Format("Привiт {name}"),
    Group(
        Start(Const("Інформація про бота"), state=InfoSG.main, id="info"),
    ),
    getter=get_name,
    state=MenuSG.main,
)

UserMainWin = Window(
    Format("Доброго дня {name}"),
    Group(
        # Start(Const("Історія пошуку"), state=UserMenuSG.search_history, id="search_history"),
        SwitchTo(Const("Нагадування"), state=UserMenuSG.remember, id="remember"),
        SwitchTo(Const("Збережені ліки"), state=UserMenuSG.favorite, id="favorite")
    ),
    getter=get_name,
    state=UserMenuSG.main,
)

FavoriteDragWin = Window(
    Const('Збережені ліки:'),
    SwitchTo(Format('{item_1}'), id="item_1", when='item_1', state=UserMenuSG.favorite_card, on_click=target_drug),
    SwitchTo(Format('{item_2}'), id="item_2", when='item_2', state=UserMenuSG.favorite_card, on_click=target_drug),
    SwitchTo(Format('{item_3}'), id="item_3", when='item_3', state=UserMenuSG.favorite_card, on_click=target_drug),
    SwitchTo(Format('{item_4}'), id="item_4", when='item_4', state=UserMenuSG.favorite_card, on_click=target_drug),
    Row(
        SwitchTo(
            Const("Назад"),
            id='previous_drug',
            state=UserMenuSG.favorite,
            on_click=previous_card,
            when='not_first_page'
        ),
        Button(Format('{max_page}'), id='max_page_len', when='max_page'),
        SwitchTo(
            Const("Вперед"),
            id='next_drug',
            state=UserMenuSG.favorite,
            on_click=next_card,
            when='not_last_page'
        ),
    ),
    Back(Const('Назад до меню')),
    state=UserMenuSG.favorite,
    getter=get_saved_drugs
)

FavoriteCardWin = Window(
    # DynamicMedia('image', when='image'),
    Multi(
        Format('{name}'),
        # Format('{description}'),
        # Format('Продається {prescriptionStatus}'),
        # Format('Ціна: {price}'),
    ),
    Group(
        Select(
            Format('{item[0]}'),
            id='telegraph_links',
            item_id_getter=operator.itemgetter(1),
            items='current_telegraph',
            on_click=link_to_favorite_telegraph
        ),
        width=1
    ),
    Row(
        Back(Const('Назад'))

    ),
    state=UserMenuSG.favorite_card,
    getter=get_drag_favorite_data
)


# TelegraphLinkWin = Window(
#     Format('{telegraph_link}'),
#     Back(Const('Назад до карточки')),
#     state=UserMenuSG.favorite_telegraph_link,
#     getter=get_telegraph_link
# )

