from enum import Enum


class ElementalDamageType(Enum):
    FIRE = ':fire:'
    ICE = ':snowflake:'
    WATER = ':droplet:'
    LIGHTNING = ':zap:'
    EARTH = ':mountain:'
    WIND = ':cloud_tornado:'

    HOLY = ':cross:'
    NECROTIC = ':skull:'


def elemental_weakness_for(element: ElementalDamageType) -> ElementalDamageType:
    m = {
        ElementalDamageType.FIRE: ElementalDamageType.WATER,
        ElementalDamageType.ICE: ElementalDamageType.FIRE,
        ElementalDamageType.WATER: ElementalDamageType.LIGHTNING,
        ElementalDamageType.LIGHTNING: ElementalDamageType.EARTH,
        ElementalDamageType.EARTH: ElementalDamageType.WIND,
        ElementalDamageType.WIND: ElementalDamageType.ICE,
    }
    return m.get(element)


class MarkdownStyle(Enum):
    BOLD = '**'
    ITALIC = '_'
    UNDERLINE = '__'


def wrap(x, w=None):
    """wrap a string
    """
    return f'{w}{x}{w}'
