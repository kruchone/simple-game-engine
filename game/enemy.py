from collections import defaultdict
from typing import Optional, List, Tuple

from game.objects import Hero
from game.util import MarkdownStyle, wrap, ElementalDamageType, elemental_weakness_for


class Enemy(object):
    """A foe to """
    fancy = MarkdownStyle.BOLD

    def __init__(self, name, hp=1, xp=3, kind: Optional[ElementalDamageType] = None):
        super().__init__()
        self.name = name
        self.max_hp = hp
        self.hp = self.max_hp
        self.xp_when_killed = xp
        self._hitmap = defaultdict(int)
        self.kind = kind

    def __str__(self):
        return f'{wrap(self.name, w=self.fancy.value)} [hp: {self.hp}]'

    def clone(self):
        return self.__class__(
            name=self.name,
            hp=self.max_hp,
            xp=self.xp_when_killed,
            kind=self.kind)

    def wound(self, player=None, damage_type: ElementalDamageType = None):
        that_really_hurt = False
        not_a_scratch = False

        damage_amount = 1

        # process weakness
        if damage_type and damage_type == elemental_weakness_for(self.kind):
            that_really_hurt = True
            damage_amount += 1

        # process resistance
        if damage_type and damage_type == self.kind:
            not_a_scratch = True
            damage_amount -= 1

        self.hp -= max(damage_amount, 0)

        if player:
            self._hitmap[player] += damage_amount

        return that_really_hurt, not_a_scratch

    def kill(self, player=None):
        if player:
            self._hitmap[player] += max(self.hp, 0)
        self.hp = 0

    def heal(self):
        self.hp = self.max_hp

    @property
    def dead(self):
        return self.hp <= 0

    def award_xp(self) -> List[Tuple[Hero, int]]:
        participation_count = len(self._hitmap.keys())
        return list(map(lambda p: (p[0], int(self.xp_when_killed/participation_count)), self._hitmap.items()))
