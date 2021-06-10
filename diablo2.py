from game.quests import Quest
from game.areas import Area
from game.enemy import Enemy
from game.util import ElementalDamageType


class Beastiary(object):
    ZOMBIE = Enemy('Zombie', hp=1, xp=3, kind=ElementalDamageType.ICE)
    FALLEN = Enemy('Fallen', hp=1, xp=3, kind=ElementalDamageType.FIRE)
    FALLEN_SHAMAN = Enemy('Fallen Shaman', hp=2, xp=5, kind=ElementalDamageType.FIRE)
    GARGANTUAN_BEAST = Enemy('Gargantuan Beast', hp=4, xp=8, kind=ElementalDamageType.ICE)

    # Bosses
    BOSS_CORPSEFIRE = Enemy('Corpsefire', hp=8, xp=80, kind=ElementalDamageType.ICE)

    # Test
    TEST = Enemy('Test Dummy', hp=2, xp=4)
    TEST_BOSS = Enemy('Large Test Dummy', hp=4, xp=12, kind=ElementalDamageType.EARTH)


QUEST_EASY_STREET = Quest('Easy Street',
                          Area('Nowhere',
                               num_enemies=1,
                               enemies={
                                   Beastiary.TEST: 100,
                               },
                               boss=Beastiary.TEST_BOSS),
                          prologue='Time for something easy to practice on...',
                          epilogue='Of course you succeeded. I expect nothing less...',
                          xp=69)

QUEST_DEN_OF_EVIL = Quest('Den of Evil',
                          Area('The Den of Evil',
                               num_enemies=24,
                               enemies={
                                   Beastiary.ZOMBIE: 10,
                                   Beastiary.FALLEN: 70,
                                   Beastiary.FALLEN_SHAMAN: 15,
                                   Beastiary.GARGANTUAN_BEAST: 5,
                               },
                               boss=Beastiary.BOSS_CORPSEFIRE),
                          prologue='You venture into the dark cave.',
                          epilogue='You emerge from the dark and bask in the light. Huzzah!',
                          xp=300)

quests = [
    QUEST_DEN_OF_EVIL,
    # QUEST_EASY_STREET,
]
