import logging
import random
from typing import Optional, Union, List, Any

from game.database import db, Hero
from game.enemy import Enemy
from game.events import FightResultEvent, SearchResultEvent, GameEvent, GameEventType, HeroEvent, GameMultiEvent
from game.exceptions import AlreadyOnQuest
from game.quests import Quest
from game.util import ElementalDamageType


logger = logging.getLogger(__name__)


class Engine(object):
    XP_FOR_SEARCHING = 1

    def __init__(self, quests=None):
        self.db = db
        self.heroes = []
        self.quests = quests
        self.current_quest: Optional[Quest] = None
        self.current_enemy: Optional[Enemy] = None
        self.game_engine = None

    def get_hero(self, name: str, discord_client_id: str = None):
        """ Add a hero to the engine.

        Args:
            name: the name of the hero to add to the game. must be unique.
            discord_client_id: the id on Discord for the user.
        """
        h, created = Hero.get_or_create(name=name,
                                        discord_client_id=discord_client_id,
                                        defaults={'hp': 20})
        if created:
            logger.info(f'New hero: {h}, ID: {h.id}')
        else:
            h.hp = 20
            h.save()
            logger.debug(f'Existing hero: {h}, ID: {h.id}')
        return h

    def start_quest(self, quest: Quest = None) -> GameEvent:
        """ Start a quest.

        Args:
            quest: the quest to start.
        """
        if self.current_quest:
            raise AlreadyOnQuest(f'You are already on quest {self.current_quest}')
        self.current_quest = quest or random.choice(self.quests)
        self.current_quest.area.populate()
        return GameEvent(GameEventType.QUEST_START, context=self.current_quest)

    def fight(self, hero: Hero, damage_type: ElementalDamageType = None,
              force_hit: bool = False, force_crit: bool = False,
              opportunity: bool = True, client_context: Any = None) -> Union[FightResultEvent, GameMultiEvent]:
        """A hero fights the current enemy"""
        fight_method_for = {
            None: self._fight_normal,
            ElementalDamageType.FIRE: self._fight_fire,
            ElementalDamageType.ICE: self._fight_ice,
            ElementalDamageType.WATER: self._fight_water,
            ElementalDamageType.LIGHTNING: self._fight_lightning,
            ElementalDamageType.EARTH: self._fight_earth,
            ElementalDamageType.WIND: self._fight_wind,
        }

        # hero turn
        try:
            verb,  hit, crit = fight_method_for[damage_type]()
        except KeyError:
            verb, hit, crit = self._fight_normal()

        crit = hit and crit  # dont allow non-hits to crit

        weak, strong = False, False
        if hit or force_hit:
            weak, strong = self.current_enemy.wound(player=hero, damage_type=damage_type)
            if crit or force_crit:
                weak = weak or self.current_enemy.wound(player=hero, damage_type=damage_type)[0]

        # enemy turn
        got_hit = False
        if not opportunity:
            if random.choice([True, False, False]):
                # you get hit
                got_hit = True
                hero.hp -= 1
                hero.save()

        fight_event = FightResultEvent(hero.hp, self.current_enemy.hp, verb=verb,
                                       hit=hit, crit=crit, weak=weak,
                                       strong=strong, enemy_hit=got_hit,
                                       hero=hero, context=client_context,
                                       enemy_context=self.current_enemy)

        # clean up the game state
        events = self.check_game_state()

        events.insert(0, fight_event)
        return GameMultiEvent(events=events)

    def _fight_normal(self):
        verb = random.choice(['swings at', 'stabs', 'smashes', 'gouges', 'stomps'])
        hit = random.choice([True, False])
        crit = random.choice([True, False, False, False])
        return verb, hit, crit

    def _fight_fire(self):
        verb = random.choice(['scorches', 'torches', 'carbonizes'])
        hit = True
        crit = random.choice([True, False, False, False, False, False, False])
        return verb, hit, crit

    def _fight_ice(self):
        verb = random.choice((['freezes', 'ices', 'chills']))
        hit = random.choice([True, False, False])
        crit = random.choice([True, False])
        return verb, hit, crit

    def _fight_water(self):
        _, hit, crit = self._fight_normal()
        verb = random.choice(['drowns', 'submerges'])
        return verb, hit, crit

    def _fight_lightning(self):
        _, hit, crit = self._fight_normal()
        verb = random.choice(['zaps', 'electrocutes'])
        return verb, hit, crit

    def _fight_earth(self):
        _, hit, crit = self._fight_normal()
        verb = random.choice(['throws a boulder at', 'chucks a sharp rock at'])
        return verb, hit, crit

    def _fight_wind(self):
        _, hit, crit = self._fight_normal()
        verb = random.choice(['channels a gust of wind at', 'summons a tornado on top of'])
        return verb, hit, crit

    def search(self, hero: Hero, client_context: Any = None) -> GameMultiEvent:
        """ Search for clues

        Args:
            hero: the hero searching
            client_context: an optional context object from the client
        """
        search_result = SearchResultEvent(hero=hero, context=client_context)
        fight_result, appear_event, boss_event = None, None, None
        if self.current_quest:
            if any(self.current_quest.area.enemies) or not self.current_quest.area.boss.dead:
                if random.choice([False, True, True]):
                    if any(self.current_quest.area.enemies):
                        # a monster appears!
                        search_result.found_enemy = True
                        self.current_enemy = self.current_enemy or self.current_quest.area.enemies.pop()
                        appear_event = GameEvent(GameEventType.ENEMY_APPEAR,
                                                 context=self.current_enemy,
                                                 message=f'{self.current_enemy} appears')
                        fight_result = self.fight(hero,
                                                  opportunity=True,
                                                  client_context=client_context)  # player gets an attack of opportunity
                        fight_result.message = f'{hero} gets an attack of opportunity on {self.current_enemy}'
                    elif not self.current_quest.area.boss.dead:
                        # the boss appears!
                        search_result.found_enemy = True
                        self.current_enemy = self.current_quest.area.boss
                        boss_event = GameEvent(GameEventType.BOSS_APPEAR, context=self.current_enemy)
                        fight_result = self.fight(hero, opportunity=True, client_context=client_context)
                        fight_result.message = f'{hero} gets an attack of opportunity on {self.current_enemy}'
                    else:
                        # no enemies and the boss is dead...
                        # fall through and just search
                        pass

        # just get search xp
        hero.xp += self.XP_FOR_SEARCHING
        hero.save()

        # tie up the events that happened
        events = [search_result]
        if appear_event:
            events.append(appear_event)
        if boss_event:
            events.append(boss_event)
        if fight_result:
            events.append(fight_result)

        return GameMultiEvent(events=events)

    def check_game_state(self) -> Optional[List[GameEvent]]:
        """ Check the game state and clean up anything that needs to be reset.
        """
        events = []

        # slain enemy, award xp
        if self.current_enemy.dead:
            events.extend(self.award_enemy_xp(self.current_enemy))
            self.current_enemy = None

        # completed quest, award xp
        if self.current_quest.complete:
            events.append(GameEvent(GameEventType.QUEST_COMPLETE, context=self.current_quest))
            for p in self.current_quest.players_participated:
                events.append(self.award_quest_xp(p, self.current_quest))
            self.current_quest = None

        return events

    def award_enemy_xp(self, enemy: Enemy) -> List[GameEvent]:
        """ Award xp when an enemy is slain.

        XP is only given out to those heroes who hit the enemy.

        Args:
            enemy: the enemy that was slain
        """
        events = []
        for hero, xp_gained in enemy.award_xp():
            hero.xp += xp_gained
            hero.save()
            events.append(HeroEvent(GameEventType.ENEMY_XP,
                                    hero=hero,
                                    context=(xp_gained, enemy)))
            self.current_quest.players_participated.add(hero)
        return events

    def award_quest_xp(self, hero: Hero, quest: Quest) -> HeroEvent:
        """ Award xp for the completion of a quest.

        Args:
            hero: the hero to award xp to
            quest: the quest completed
        """
        amt = quest.xp_upon_completion
        hero.xp += amt
        hero.save()
        return HeroEvent(GameEventType.QUEST_XP, hero=hero, context=(amt, quest))

    def score(self) -> GameEvent:
        scores = [(str(h), h.xp) for h in Hero.select().where(Hero.xp > 0).order_by(Hero.xp.desc())]
        return GameEvent(GameEventType.SCORE, context=scores)

    def process_event(self, event: GameEvent) -> GameEvent:
        if event.type == GameEventType.SEARCH:
            if isinstance(event, HeroEvent):
                return self.search(event.hero, client_context=event.context)
        elif event.type == GameEventType.FIGHT:
            if isinstance(event, HeroEvent):
                return self.fight(event.hero, damage_type=event.augment, client_context=event.context)
        elif event.type == GameEventType.COMMAND:
            if event.message == 'quest start':
                # picks a random quest to start if none supplied.
                try:
                    return self.start_quest()
                except AlreadyOnQuest:
                    return GameEvent(GameEventType.QUEST_GET_CURRENT, context=self.current_quest)
            elif event.message == 'quest':
                return GameEvent(GameEventType.QUEST_GET_CURRENT, context=self.current_quest)
            elif event.message == 'quest abandon':
                self.current_quest = None
                return GameEvent(GameEventType.QUEST_ABANDON)
            elif event.message == 'score':
                return self.score()
            else:
                return GameEvent(GameEventType.NOOP)
        else:
            return GameEvent(GameEventType.NOOP)
