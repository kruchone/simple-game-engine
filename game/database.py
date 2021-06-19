import os
import datetime
import uuid

from pathlib import Path
from peewee import Model, SqliteDatabase, UUIDField, CharField, DateTimeField, IntegerField

project_root = Path(__file__).parent.parent.absolute()
db = SqliteDatabase(os.path.join(project_root, 'game.db'))


class GameModel(Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4)

    class Meta:
        database = db


class Hero(Model):
    name = CharField(null=False, unique=True)
    xp = IntegerField(null=False, default=0)
    hp = IntegerField(null=False)
    join_date = DateTimeField(default=datetime.datetime.utcnow())
    discord_client_id = CharField(null=True, unique=True)

    class Meta:
        database = db

    def as_dict(self):
        return {
            'name': self.name,
            'xp': self.xp,
            'hp': self.hp
        }

    def __str__(self):
        return self.name


if __name__ == '__main__':
    print('Making table.')
    db.connect()
    db.create_tables([Hero], safe=True)
    print('Done.')
