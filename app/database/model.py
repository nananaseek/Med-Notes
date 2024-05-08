from tortoise import Model, fields


class BaseModel:
    id = fields.UUIDField(pk=True)


class User(BaseModel, Model):
    telegram_id = fields.BigIntField()
    name = fields.CharField(max_length=255)
    med: fields.ReverseRelation["Pills"]
    drugs_history: fields.ReverseRelation["SearchPils"]


class Pills(BaseModel, Model):
    user: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField(
        "models.User", related_name="med_user")
    name = fields.CharField(max_length=208)
    is_remember = fields.DatetimeField(null=True)
    favorite = fields.BooleanField(default=False)
    url = fields.CharField(max_length=128, null=True)


class SearchPils(BaseModel, Model):
    user: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField(
        "models.User", related_name="user_search")
    url = fields.CharField(max_length=64)
    name = fields.CharField(max_length=32)
    search_query = fields.CharField(max_length=32)

