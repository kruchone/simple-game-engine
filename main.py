import logging
import os

from game.ext.discord_client import DiscordClient
from game.engine import Engine

import diablo2


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logging.getLogger('discord').setLevel(logging.INFO)


if __name__ == '__main__':
    engine = Engine(quests=diablo2.quests)
    bot = DiscordClient(engine=engine)
    bot.run(os.environ.get('BOT_TOKEN'), bot=True)
