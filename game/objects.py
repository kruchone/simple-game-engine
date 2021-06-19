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
