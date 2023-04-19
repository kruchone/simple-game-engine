import random
from collections import defaultdict

from game.enemy import Enemy


class Area(object):
    def __init__(self,
                 name: str,
                 num_enemies: int,
                 enemies: dict = None,
                 boss: Enemy = None,
                 prologue: str = None,
                 epilogue: str = None):
        self.name = name
        self._probabilities = enemies or {}
        self.enemies = []
        self.num_enemies = num_enemies
        self.boss = boss.clone()
        self.populate()
        self.prologue = prologue or 'The heroes enter ' + self.name
        self.epilogue = epilogue or 'The heroes leave ' + self.name

    def __str__(self):
        s = self.name
        if any(self.enemies):
            s += f' (enemies: {len(self.enemies) + 1})'
        if self.boss:
            s += f' (boss: {self.boss})'
        if not any(self.enemies) and not self.boss:
            s += ' (empty)'
        return s

    def spawn_random_enemy(self):
        enemy = random.choices(
            list(self._probabilities.keys()),
            list(map(lambda p: p / 100, self._probabilities.values())))[0]
        self.enemies.append(enemy.clone())

    def populate(self):
        for spawn in range(self.num_enemies - 1):
            self.spawn_random_enemy()
        self.boss.heal()

    def enemy_count(self):
        counts = defaultdict(int)
        for e in self.enemies:
            counts[e.name] += 1
        for enemy, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
            print(f'{count} {enemy}')
