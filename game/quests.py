from game.areas import Area
from game.util import MarkdownStyle, wrap


class Quest(object):
    fancy = MarkdownStyle.UNDERLINE

    def __init__(self, name: str, area: Area, prologue: str = None, epilogue: str = None, xp: int = None):
        self.name = name
        self.area = area
        self.prologue = prologue
        self.epilogue = epilogue
        self.xp_upon_completion = xp or 0

        self.players_participated = set()

    def __str__(self):
        return wrap(self.name, w=self.fancy.value)

    @property
    def complete(self):
        return len(self.area.enemies) == 0 and self.area.boss.dead
