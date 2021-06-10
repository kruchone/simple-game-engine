from enum import Enum
from typing import Any, List

from game.objects import Location, GameObject, Hero


class GameEventType(Enum):
    SEARCH = 1
    FIGHT = 2
    COMMAND = 3

    NOOP = 4

    QUEST_START = 5
    QUEST_GET_CURRENT = 6
    QUEST_ABANDON = 7
    QUEST_COMPLETE = 8
    QUEST_XP = 9

    ENEMY_APPEAR = 10
    ENEMY_XP = 11

    BOSS_APPEAR = 12

    MULTI = 13

    SCORE = 14


class GameEvent(object):
    """represents something happening in the game

    Args:
        t: the type of event this is
        location: the location the event happened at
        augment: the augmentation for the event, to change its behavior in the engine
        context: the calling context of the event
        message: the string message of the event
    """
    def __init__(self, t: GameEventType,
                 location: Location = None,
                 augment: GameObject = None,
                 context: Any = None,
                 message: str = None):
        self.type = t
        self.augment = augment
        self.location = location
        self.message = message
        self.context = context

    def __str__(self):
        return f'event.{self.type.name}: {self.message if self.message else "(no message)"}'

    def add_augment(self, obj: GameObject) -> None:
        """augment an event with a game object
        """
        self.augment = obj


class GameMultiEvent(GameEvent):
    """ Multiple things happening in one event.

    Contextually treat the event in timeline-order. That is, [0] is the first
    thing that happened, followed by [1].
    """
    def __init__(self, events: List[GameEvent]):
        super().__init__(GameEventType.MULTI)
        self.events = events


class HeroEvent(GameEvent):
    """an event that involves a hero

    NOTE: This does not supply `engine` argument to the GameEvent,
          so you cannot use this event directly, it is essentially abstract.
    """
    def __init__(self, t: GameEventType, hero: Hero, **kwargs):
        self.hero = hero
        super().__init__(t, **kwargs)


class SearchResultEvent(HeroEvent):
    """results of a search action

    Args:
        found_enemy: whether the hero found an enemy
    """
    def __init__(self, found_enemy: bool = False, **kwargs):
        self.found_enemy = found_enemy
        super().__init__(GameEventType.SEARCH, **kwargs)


# TODO: maybe move this into contexts.py
class EntityFightContext(object):
    """something happened to an entity during a fight. this is the aftermath
    """
    def __init__(self, hp: int = None,
                 hit: bool = False, crit: bool = False,
                 weak: bool = False, strong: bool = False,
                 context: Any = None):
        self.hp = hp
        self.hit = hit
        self.crit = crit
        self.weak = weak
        self.strong = strong
        self.context = context


class FightResultEvent(HeroEvent):
    """The result of a fight event.

    Args:
        hp: the hero's hp after the fight
        enemy_hp: the enemy's hp after the fight
        hit: if the hero hit
        crit: if the hero crit
        weak: if the hero used an attack the enemy was weak to
        strong: if the hero used an attack the enemy was resistant to
        enemy_hit: if the enemy hit the hero
        enemy_crit: if the enemy crit the hero
        enemy_weak: if the enemy used an attack the hero was weak to
        enemy_strong: if the enemy used an attack the hero was resistant to
        hero_context: the client's context for the hero portion of the event
        enemy_context: the client's context for the enemy portion of the event
    """
    def __init__(self, hp: int,
                 enemy_hp: int,
                 hit: bool = False,
                 crit: bool = False,
                 weak: bool = False,
                 strong: bool = False,
                 enemy_hit: bool = False,
                 enemy_crit: bool = False,
                 enemy_weak: bool = False,
                 enemy_strong: bool = False,
                 **kwargs):
        self.verb = kwargs.pop('verb', 'hit')
        self.hero_result = EntityFightContext(hp=hp, hit=hit, crit=crit, weak=weak, strong=strong,
                                              context=kwargs.get('hero_context'))
        self.enemy_result = EntityFightContext(hp=enemy_hp, hit=enemy_hit, crit=enemy_crit,
                                               weak=enemy_weak, strong=enemy_strong,
                                               context=kwargs.pop('enemy_context', None))
        super().__init__(GameEventType.FIGHT, **kwargs)
