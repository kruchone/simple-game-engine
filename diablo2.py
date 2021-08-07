from game.quests import Quest
from game.areas import Area
from game.enemy import Enemy
from game.util import ElementalDamageType


class Beastiary(object):
    ZOMBIE = Enemy('Zombie', hp=1, xp=3)
    ZOMBIE_2 = Enemy('Hungry Dead', hp=3, xp=7)
    GHOUL = Enemy('Ghoul', hp=3, xp=6, kind=ElementalDamageType.NECROTIC)

    SKELETON = Enemy('Skeleton', hp=2, xp=4)
    SKELETAL_ARCHER = Enemy('Skeletal Archer', hp=4, xp=7)

    FALLEN = Enemy('Fallen', hp=1, xp=3, kind=ElementalDamageType.FIRE)
    FALLEN_SHAMAN = Enemy('Fallen Shaman', hp=2, xp=5, kind=ElementalDamageType.FIRE)

    CARVER = Enemy('Carver', hp=2, xp=7, kind=ElementalDamageType.ICE)
    CARVER_SHAMAN = Enemy('Carver Shaman', hp=5, xp=8, kind=ElementalDamageType.ICE)

    DARK_ONE = Enemy('Dark One', hp=3, xp=10)
    DARK_SHAMAN = Enemy('Dark Shaman', hp=6, xp=11)

    GARGANTUAN_BEAST = Enemy('Gargantuan Beast', hp=4, xp=8, kind=ElementalDamageType.ICE)
    AFFLICTED = Enemy('Afflicted', hp=6, xp=12, kind=ElementalDamageType.LIGHTNING)
    THE_BANISHED = Enemy('The Banished', hp=8, xp=16, kind=ElementalDamageType.LIGHTNING)

    # Bosses
    BOSS_CORPSEFIRE = Enemy('Corpsefire', hp=8, xp=80, kind=ElementalDamageType.ICE)
    BOSS_BLOOD_RAVEN = Enemy('Blood Raven', hp=12, xp=100, kind=ElementalDamageType.WIND)
    BOSS_GRISWOLD = Enemy('Griswold', hp=16, xp=160)
    BOSS_ANDARIEL = Enemy('Andariel', hp=25, xp=300, kind=ElementalDamageType.NECROTIC)

    # Test
    TEST = Enemy('Test Dummy', hp=2, xp=4)
    TEST_BOSS = Enemy('Large Test Dummy', hp=4, xp=12, kind=ElementalDamageType.EARTH)


pl = """
The party arrives at the Rogue encampment, a makeshift town cobbled together after Diablo's forces attacked the nearby \
Rogue Monastery. A woman in priestess clothing approaches the heroes. Hearing that your party is willing to offer \
assistance to the town, she mentions a nearby underground den filled with horrors.

"There is a place of great evil in the wilderness. Kashya's Rogue scouts have informed me that a cave nearby is filled \
with shadowy creatures and horrors from beyond the grave. I fear that these creatures are massing for an attack \
against our encampment. If you are sincere about helping us, find the dark labyrinth and destroy the foul beasts. \
May the Great Eye watch over you."

Your heroes head to the wilderness in search of this Den of Evil.
"""

el = """
Akara is smiling as the heroes return to the Rogue Encampment.

"You have cleansed the Den of Evil. You've earned my trust and may yet restore my faith in humanity. \
I will let Kashya know of your good deed."
"""

QUEST_DEN_OF_EVIL = Quest('Den of Evil',
                          Area('The Den of Evil',
                               prologue='The party finds the Den after hours searching in the Blood Moor. '
                                        'As the heroes descend, the air becomes thick and wet, making it harder to '
                                        'breathe. You hear sounds of distant demonic babbling.',
                               num_enemies=24,
                               enemies={
                                   Beastiary.ZOMBIE: 10,
                                   Beastiary.FALLEN: 70,
                                   Beastiary.FALLEN_SHAMAN: 15,
                                   Beastiary.GARGANTUAN_BEAST: 5,
                               },
                               boss=Beastiary.BOSS_CORPSEFIRE,
                               epilogue='The heroes slay every last beast in the Den. After only a brief moment to '
                                        'tend to any wounds, the party heads back to the surface.'),
                          prologue=pl, epilogue=el, xp=300)

pl = """
Kashya, town field captain, has heard of your successful cleansing of the Den of Evil. She approaches the party.

"My Rogue scouts have just reported an abomination in the Monastery graveyard! Apparently, Andariel is not content \
to take only our living. Blood Raven, one of our finest captains in the battle against Diablo at Tristram, was also \
one of the first to be corrupted by Andariel. Now, you'll find her in the Monastery graveyard raising our dead as \
zombies! We cannot abide this defilement! If you are truly our ally, you will help us destroy her..."
"""

el = """
The party returns to Kashya after vanquishing Blood Raven.

"I can hardly believe that you've defeated Blood Raven! Though she was once my closest friend, I pray that her \
tortured spirit remains banished forever. You have earned my respect, stranger...and the allegiance of the Rogues."
"""
QUEST_SISTERS_BURIAL_GROUNDS = Quest('Sisters\' Burial Grounds',
                                     Area('Burial Grounds',
                                          prologue='The group sets forth to the lands beyond the Blood Moor, through '
                                                   'the Cold Plains and onto the Burial Grounds. Once a respected '
                                                   'place within the Sisterhood, it is now desecrated.',
                                          num_enemies=15,
                                          enemies={
                                              Beastiary.SKELETON: 50,
                                              Beastiary.ZOMBIE_2: 50,
                                          },
                                          boss=Beastiary.BOSS_BLOOD_RAVEN,
                                          epilogue='After Blood Raven is vanquished, a calmness falls over the Burial '
                                                   'Grounds. What is left of the dead may rest in peace once more.'),
                                     prologue=pl, epilogue=el, xp=550)


pl = """
Akara, seeing your party's strength in defeating Blood Raven, approaches the group.

"It is clear that we are facing an Evil difficult to comprehend, let alone combat. There is only one Horadrim sage, \
schooled in the most arcane history and lore, who could advise us...His name is Deckard Cain. You must go to Tristram \
and find him, my friend. I pray that he still lives."
"""

el = """
Returning to Town with Deckard Cain, Akara meets you.

"You have risked your life to rescue Cain. For that we thank you. We must seek his counsel, just as soon as we make
sure he is okay."

After Deckard Cain is patched up by the Rogue medics, you learn what he knows. He speaks slowly, but with confidence.

"Regrettably, I could do nothing to prevent the disaster which devastated Tristram. It would appear that our greatest \
fears have come to pass. Diablo, the Lord of Terror, has once again been set loose upon the world!

As you know, some time ago Diablo was slain beneath Tristram. And when our hero emerged triumphant from the labyrinth \
beneath town, we held a grand celebration that lasted several days.

Yet, as the weeks passed, our hero became increasingly aloof. He kept his distance from the rest of the townsfolk and \
seemed to lapse into a dark, brooding depression. I thought that perhaps his ordeal had been so disturbing that he \
simply could not put it out of his mind.

The hero seemed more tormented every passing day. I remember he awoke many times - screaming in the night - always \
something about 'the East'.

One day, he simply left. And shortly thereafter, Tristram was attacked by legions of foul demons. Many were slain, 
and the demons left me to die in that cursed cage.

I believe now that Tristram's hero was that Dark Wanderer who passed this way before the Monastery fell.

I fear even worse, my friend...I fear that Diablo has taken possession of the hero who sought to slay him. If true, \
Diablo will become more powerful than ever before.

You must stop him or all will be lost."
"""
QUEST_SEARCH_FOR_CAIN = Quest('Search for Cain',
                              Area('Tristram',
                                   prologue='The party treks to the lands of Old Tristram. The air is hot and almost '
                                            'everything is charred black, some buildings still smoldering.',
                                   num_enemies=25,
                                   enemies={
                                       Beastiary.SKELETON: 25,
                                       Beastiary.SKELETAL_ARCHER: 15,
                                       Beastiary.ZOMBIE_2: 25,
                                       Beastiary.FALLEN: 20,
                                       Beastiary.FALLEN_SHAMAN: 15,
                                   },
                                   boss=Beastiary.BOSS_GRISWOLD,
                                   epilogue='Just in time, the Heroes rescue Deckard Cain from a makeshift prison cell '
                                            'hoisted into the air. Only the Prime Evils themselves know what they '
                                            'had planned for one of the last of the Horadrim. You toss him a town '
                                            'town portal scroll which he casts. Jumping through the newly opened '
                                            'portal, the party escapes back to the Rogue Encampment.'),
                              prologue=pl, epilogue=el, xp=550)




pl = """
The party returns to Deckard Cain. It seems he has been busy researching the plague that haunts the Rogue Encampment \
and surrounding areas.

"It is certain that we face the demon queen, Andariel, who has corrupted the Rogue Sisterhood and defiled their \
ancestral Monastery. This does not bode well for us, my friend. Ancient Horadric texts record that Andariel and the \
other Lesser Evils once overthrew the three Prime Evils - Diablo, Mephisto and Baal - banishing them from Hell to our \
world. Here, they caused mankind untold anguish and suffering before they were finally bound within the Soulstones. \
Andariel's presence here could mean that the forces of Hell are once again aligned behind Diablo and his Brothers. \
If this is true, then I fear for us all. You must kill her before the Monastery becomes a permanent outpost of Hell \
and the way east lost forever."

After some last minute trades, the heroes head to the Monastery Catacombs, the presumed location of Andariel.
"""

el = """
The heroes return after defeating Andariel. Kashya is waiting for them with a large smile on her face.
"Andariel's death brings about renewed life for us all. We mourn the loss of our dear Sisters, but at least now we can \
get on with our lives. I...may have misjudged you, outlander. You are a true hero and testament to the noble spirit \
which has inspired our Order for generations. Fare well...my friend."

Warriv walks over to the party and lets them know the path is now clear.
"The caravan is prepared. We may now journey eastward to Lut Gholein."
"""
SISTERS_TO_THE_SLAUGHTER = Quest('Sisters to the Slaughter',
                           Area('The Catacombs',
                                prologue='The party heads deep into the monastery Catacombs- the source from which '
                                         'the undead seem to be emanating.',
                                num_enemies=50,
                                enemies={
                                    Beastiary.DARK_ONE: 30,
                                    Beastiary.AFFLICTED: 20,
                                    Beastiary.GHOUL: 25,
                                    Beastiary.THE_BANISHED: 10,
                                    Beastiary.DARK_SHAMAN: 15,
                                },
                                boss=Beastiary.BOSS_ANDARIEL,
                                epilogue='The party makes the long trek back to the surface. It will be great to see '
                                         'the light once more...'),
                           prologue=pl, epilogue=el, xp=550)

quests = [
    # Act I
    # QUEST_DEN_OF_EVIL,
    QUEST_SISTERS_BURIAL_GROUNDS,
    QUEST_SEARCH_FOR_CAIN,
    # TODO: Search for Cain.
    # TODO: Forgotten Tower.
    SISTERS_TO_THE_SLAUGHTER,
]
