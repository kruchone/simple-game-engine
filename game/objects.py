from enum import Enum
from typing import Any


class GameObject(object):
    def __init__(self, context: Any = None):
        self.context = context


class ElementalDamageType(GameObject, Enum):
    FIRE = ':fire:'
    ICE = ':snowflake:'
    WATER = ':droplet:'
    LIGHTNING = ':zap:'
    EARTH = ':mountain:'
    WIND = ':cloud_tornado:'

    HOLY = ':cross:'
    NECROTIC = ':skull:'


class Location(GameObject, Enum):
    TOWN = 'town'
    WILDERNESS = 'wilderness'


class Hero(GameObject):
    def __init__(self, name: str, **kwargs):
        self.name = name
        self.hp = kwargs.get('hp', 20)
        self.xp = kwargs.get('xp', 0)
        super().__init__(**kwargs)

    def as_dict(self):
        return {
            'name': self.name,
            'xp': self.xp,
            'hp': self.hp
        }

    def __str__(self):
        return self.name
