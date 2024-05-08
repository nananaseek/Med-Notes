from aiogram.fsm.state import StatesGroup, State


class RegistrationSG(StatesGroup):
    main = State()
    login = State()
    password = State()


class MenuSG(StatesGroup):
    main = State()


class UserMenuSG(StatesGroup):
    main = State()
    # search_history = State()
    remember = State()
    favorite = State()
    favorite_card = State()
    favorite_telegraph = State()
    favorite_telegraph_link = State()


class InfoSG(StatesGroup):
    main = State()


class SearchDrugsSG(StatesGroup):
    get_query = State()
    progress = State()
    drug_card = State()
    drug_card_info = State()
    telegraph_link = State()
    when = State()


class ProgressSG(StatesGroup):
    progress = State()


class DrugCardSG(StatesGroup):
    main = State()
