import datetime

from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from app.database.model import User, Pills, SearchPils

get_user = pydantic_model_creator(User, name="get_user")
create_user = pydantic_model_creator(User, name="create_user")

get_pills = pydantic_model_creator(Pills, name="get_pills")
create_pill = pydantic_model_creator(Pills, name="create_pill")

get_user_search = pydantic_model_creator(SearchPils, name="get_user_search")
create_user_search = pydantic_model_creator(SearchPils, name="create_user_search", exclude=("id", 'user'))


class UpdatePills(BaseModel):
    is_remember: datetime.datetime
    favorite: bool
