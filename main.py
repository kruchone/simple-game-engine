import logging
import os

from game.database import db
from game.ext.discord_client import DiscordClient
from game.engine import Engine

import diablo2


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logging.getLogger('discord').setLevel(logging.INFO)
logging.getLogger('peewee').setLevel(logging.INFO)


if __name__ == '__main__':
    db.connect()
    engine = Engine(quests=diablo2.quests)
    bot = DiscordClient(engine=engine)
    try:
        bot.run(os.environ.get('BOT_TOKEN'), reconnect=True)
    except KeyboardInterrupt:
        db.close()
        print('Done!')
