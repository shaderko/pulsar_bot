from enum import unique
from mongoengine import Document, StringField, IntField, ListField, DictField, DateField


class Item(Document):
    name = StringField()
    desc = StringField()
    iid = IntField(unique=True)


class Game(Document):
    name = StringField()
    time = IntField()
    gid = IntField(unique=True)


class Member(Document):
    uid = IntField(unique=True, required=True)
    xp = IntField()
    lvl = IntField()
    items = ListField(Item)
    games = DictField()
    birthday = DateField()