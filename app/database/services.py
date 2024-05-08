from typing import TypeVar, Union
from tortoise import Model
from pydantic import BaseModel

from app.database import model, schemas

ModelType = TypeVar("ModelType", bound=Model)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
GetSchemaType = TypeVar("GetSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseServices:
    model = ModelType
    create_schema = CreateSchemaType
    update_schema = UpdateSchemaType
    get_schema = GetSchemaType

    async def create(self, schema: create_schema, **kwargs) -> ModelType:
        return await self.model.create(**schema.model_dump(exclude_unset=True), **kwargs)

    async def get(self, **kwargs) -> ModelType:
        return await self.model.get(**kwargs)

    async def delete(self, **kwargs) -> None:
        return await self.model.delete(**kwargs)

    async def all(self) -> list[ModelType]:
        return await self.model.all()


class PillsServices(BaseServices):
    model = model.Pills
    create_schema = schemas.create_pill
    get_schema = schemas.get_pills
    update_schema = schemas.UpdatePills


class UsersServices(BaseServices):
    model = model.User
    create_schema = schemas.create_user
    get_schema = schemas.get_user

    async def is_registered(self, telegram_id: int):
        return await self.model.get_or_none(telegram_id=telegram_id)

    async def register(self, telegram_id, name):
        await self.model(telegram_id=telegram_id, name=name).save()

    async def get_by_tg(self, telegram_id: int):
        return await self.model.get_or_none(telegram_id=telegram_id)

    async def get_count(self) -> int:
        return await self.model.all().count()


class SearchPillsServices(BaseServices):
    model = model.SearchPils
    create_schema = schemas.create_user_search
    get_schema = schemas.get_user_search

    async def create(self, schema: create_schema, **kwargs):
        user = await user_services.get(telegram_id=kwargs['user_id'])
        history = await self.model(**schema.model_dump())
        history.user = user
        await history.save()

    async def get_saved_drugs(
            self,
            user_id: int,
            page: int = 1,
            object_per_page: int = 10,
    ) -> dict:
        user = await user_services.get(telegram_id=user_id)
        obj = self.model.filter(user_id=user.id)
        pagination = await obj.offset((page - 1) * object_per_page).limit(object_per_page).all()
        objects_count = await obj.count()
        return {
            'pagination': pagination,
            'objects_count': objects_count
        }

    async def is_saved_url(
            self,
            url: str
    ):
        return self.model.get_or_none(url=url)


user_services = UsersServices()
search_services = SearchPillsServices()
