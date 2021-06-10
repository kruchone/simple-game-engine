import logging

from typing import Optional

from game import events
from game.engine import Engine
from game.objects import Location


logger = logging.getLogger(__name__)


class GameClient(object):
    def __init__(self, **kwargs):
        logger.debug('Setting up game client.')
        self.engine: Engine = kwargs.pop('engine')
        self.town: Optional[Location] = None
        self.wilderness: Optional[Location] = None

    async def emit(self, event: events.GameEvent):
        """ Prints out a game event

        You probably want to override this if you are making a subclass of `GameClient`.

        Args:
            event: the event to print
        """
        if event.message:
            if event.location:
                logger.info(f'{event.location.name}> {event.message}')
            else:
                logger.info(f'{event.message}')

    async def absorb(self, event: events.GameEvent):
        """ Ingest an event into the engine."""
        result = self.engine.process_event(event)
        return await self.emit(result)
