import logging
import random

from collections import namedtuple
from enum import Enum
from queue import Queue
from typing import Optional, Dict

from game import events
from game.database import Hero
from game.client import GameClient
from game.util import wrap, ElementalDamageType
from game.objects import Location

# noinspection PyPackageRequirements
import discord


class Emoji(Enum):
    """Emojis and their discord text representations.

    Most of these have corresponding unicode counterparts, but these can be used inside the message text
    just as you do using Discord normally. These will not compare properly for incoming messages.

    TODO: combine this with `emojis` (below)
    """
    SWING = ':axe:'
    ATTACK_HIT = ':boom:'
    ATTACK_MISS = ':dash:'
    ATTACK_CRIT = ':star2:'
    DAMAGE = ':drop_of_blood:'

    ENEMY = ':japanese_ogre:'
    DEAD = ':skull_crossbones:'

    PLACE_1 = ':first_place:'
    PLACE_2 = ':second_place:'
    PLACE_3 = ':third_place:'


# discord uses some wonky (out-of-date?) emojis, so compare by bytes
# https://stackoverflow.com/questions/47716217/converting-emojis-to-unicode-and-vice-versa-in-python-3
# https://github.com/discord/discord-api-docs/issues/2723
emoji = namedtuple('emoji', ['str', 'enum', 'discord'])
emojis = [
    emoji(str='🔥', enum=ElementalDamageType.FIRE, discord=b'\xf0\x9f\x94\xa5'),
    emoji(str='❄', enum=ElementalDamageType.ICE, discord=b'\xe2\x9d\x84\xef\xb8\x8f'),
    emoji(str='💧', enum=ElementalDamageType.WATER, discord=b'\xf0\x9f\x92\xa7'),
    emoji(str='⚡', enum=ElementalDamageType.LIGHTNING, discord=b'\xe2\x9a\xa1'),
    emoji(str='⛰', enum=ElementalDamageType.EARTH, discord=b'\xe2\x9b\xb0\xef\xb8\x8f'),
    emoji(str='🌪️', enum=ElementalDamageType.WIND, discord=b'\xf0\x9f\x8c\xaa\xef\xb8\x8f')
]


logger = logging.getLogger(__name__)


class DiscordClient(GameClient, discord.Client):
    SERVER_NAME = 'A Professional Farmer'
    CHANNEL_TOWN_NAME = 'town'
    CHANNEL_WILDERNESS_NAME = 'wilderness'
    ROLE_NAME = 'Hero'

    def __init__(self, **kwargs):
        self.game_server: Optional[discord.Guild] = None
        self.town: Optional[discord.TextChannel] = None
        self.wilderness: Optional[discord.TextChannel] = None
        self.hero_role: Optional[discord.Role] = None

        # Keep track of which member is which Hero
        self.member_to_hero: Dict[discord.Member, Hero] = {}

        bot_intents = discord.Intents.default()
        bot_intents.members = True
        # kwargs['intents'] = bot_intents

        # HACK: can't I just use super().__init__(**kwargs) ? I guess not
        # TODO: figure out how to just use super() normally.
        discord.Client.__init__(self, intents=bot_intents)
        GameClient.__init__(self, **kwargs)
        # super().__init__(**kwargs)

    async def on_ready(self):
        """ Called when the discord client is ready to begin, all connections are established.
        """
        self.game_server = next((g for g in self.guilds if g.name == self.SERVER_NAME), None)
        if self.game_server:
            self.town = next((ch for ch in self.game_server.channels if ch.name == self.CHANNEL_TOWN_NAME), None)
            self.wilderness = next((ch for ch in self.game_server.channels if ch.name == self.CHANNEL_WILDERNESS_NAME), None)
            self.hero_role = next((r for r in self.game_server.roles if r.name == self.ROLE_NAME), None)
            if self.engine and self.town and self.wilderness:
                # add hero players
                for member in self.hero_role.members:
                    # TODO: listen for players joining Hero role and add them in
                    logger.info(f'Getting Hero {member.name} for Discord member: {member} ({member.id})')
                    new_hero = self.engine.get_hero(member.name, discord_client_id=str(member.id))
                    self.member_to_hero[member] = new_hero

    async def on_message(self, message: discord.Message):
        """ Called when a message is sent in discord.
        """
        # ignore messages from the bot itself
        if self.user == message.author:
            return

        # add the hero to the engine if they are not already
        if message.channel in (self.wilderness, self.town):
            if message.author in self.hero_role.members and message.author not in self.member_to_hero.keys():
                new_hero = self.engine.get_hero(message.author.name, discord_client_id=str(message.author.id))
                self.member_to_hero[message.author] = new_hero

        # make game event from message
        event = None
        if message.channel == self.wilderness:
            location = Location.WILDERNESS
            if self.engine.current_enemy:
                # fight
                event = events.HeroEvent(
                    events.GameEventType.FIGHT,
                    hero=self.member_to_hero[message.author],
                    message=str(message.clean_content),
                    location=location,
                    context=message)
                augment = next((e for e in emojis if e.discord.decode('utf-8') == message.clean_content), None)
                if augment:
                    # TODO: why does typehinting not work for child classes? am I doing something wrong?
                    #   either way this works just fine.
                    event.add_augment(augment.enum)
            else:
                # search
                event = events.HeroEvent(
                    events.GameEventType.SEARCH,
                    hero=self.member_to_hero[message.author],
                    message=str(message.clean_content),
                    location=location,
                    context=message)

        elif message.channel == self.town:
            # command
            event = events.HeroEvent(
                events.GameEventType.COMMAND,
                hero=self.member_to_hero[message.author],
                message=str(message.clean_content),
                location=Location.TOWN,
                context=message)

        # send it
        if event:
            await self.absorb(event)
        else:
            logger.debug(f'No event captured for message "{message.clean_content}"')

    async def emit(self, event: events.GameEvent):
        """ Called when a game event happens.

        Prints out the state of what just happened.

        Args:
            event: the event that occurred
        """
        # origin_event = event
        event_queue = Queue()
        event_queue.put(event)
        while not event_queue.empty():
            event = event_queue.get()

            # Multi
            if isinstance(event, events.GameMultiEvent):
                for e in event.events:
                    event_queue.put(e)
            # SearchResult
            elif isinstance(event, events.SearchResultEvent):
                if not event.found_enemy:
                    await event.context.add_reaction('🔍')
            # FightResult
            elif isinstance(event, events.FightResultEvent):
                fight_result_message = ''
                if event.hero_result.hit:
                    fight_result_message += wrap(f'{event.hero} {event.verb} {event.enemy_result.context.name}!',
                                                 w=Emoji.ATTACK_HIT.value)
                else:
                    await event.context.add_reaction('💨')
                if event.hero_result.crit:
                    fight_result_message += f'... and it\'s a critical hit {Emoji.ATTACK_CRIT.value}!!!'
                    await event.context.add_reaction('🌟')
                if event.hero_result.hit or event.hero_result.crit:
                    await self.wilderness.send(fight_result_message)

                # enemy weaknesses and resistances
                if event.hero_result.weak:
                    await self.wilderness.send(f'{event.enemy_result.context} writhes in pain!')
                if event.hero_result.strong:
                    await self.wilderness.send(f'{event.enemy_result.context} doesn\'t seem to be affected that much...')

                # enemy death
                if event.enemy_result.hp <= 0:
                    death_animation = random.choice(['collapses', 'dies'])
                    await self.wilderness.send(wrap(f'{event.enemy_result.context} {death_animation}.', w=Emoji.DEAD.value))

                # hero damage
                if event.enemy_result.hit:
                    await event.context.add_reaction('🩸')
                    # player hp indicator
                    indicator = {9: '9️⃣', 8: '8️⃣', 7: '7️⃣', 6: '6️⃣', 5: '5️⃣', 4: '4️⃣',
                                 3: '3️⃣', 2: '2️⃣', 1: '1️⃣', 0: '☠'}
                    if indicator.get(event.hero_result.hp):
                        await event.context.add_reaction(indicator.get(event.hero_result.hp))

                # hero death
                if event.hero_result.hp <= 0:
                    await self.town.send(wrap(f'{event.hero_result.context} died.',
                                              w=Emoji.DEAD.value))
            # Other less-complex events
            elif event.type is events.GameEventType.QUEST_START:
                await self.town.send(f'Starting quest "{event.context}".')
                await self.wilderness.send(event.context.prologue)
            elif event.type is events.GameEventType.QUEST_GET_CURRENT:
                await self.town.send(f'Currently on the quest "{event.context}".')
            elif event.type is events.GameEventType.QUEST_ABANDON:
                await self.town.send('If you say so...')
            elif event.type is events.GameEventType.QUEST_COMPLETE:
                await self.wilderness.send(event.context.epilogue)
                await self.town.send(f'Our Heroes have completed the quest "{event.context}".')
            elif event.type is events.GameEventType.QUEST_XP:
                await self.town.send(f'{event.hero} gets {event.context[0]} xp '
                                     f'for helping with the quest: "{event.context[1]}"')
            elif event.type is events.GameEventType.ENEMY_APPEAR:
                kind = event.context.kind and event.context.kind.value or ''
                await self.wilderness.send(f'Out of nowhere! {Emoji.ENEMY.value} {event.context} {kind}')
            elif event.type is events.GameEventType.BOSS_APPEAR:
                kind = event.context.kind and event.context.kind.value or ''
                await self.wilderness.send(f'From the shadows comes a formidable foe, "{event.context}" {kind}!')
            elif event.type is events.GameEventType.ENEMY_XP:
                await self.wilderness.send(f'{event.hero} received [{event.context[0]}] xp '
                                           f'for helping to fight {event.context[1].name}')
            elif event.type is events.GameEventType.SCORE:
                awards = iter([Emoji.PLACE_1, Emoji.PLACE_2, Emoji.PLACE_3])
                for hero, score in event.context:
                    a = next(awards, None)
                    await self.town.send(f'{a.value if a else ""} {hero}: {score}')

            await super().emit(event)
