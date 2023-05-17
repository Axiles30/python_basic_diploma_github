from peewee import *

# from peewee import SqliteDatabase, Model, CharField, IntegerField
db = SqliteDatabase('database.db')


# Создали класс, чтобы наследовать от него все таблицы базы данных
class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    # В классе описываем таблицу в базе данных
    name = CharField()
    telegram_id = IntegerField()


