
Playing the game
===

The following document explains how to play the game. It assumes the user 
is interacting with the Discord client.

Getting access to the game
---

Once you are granted the Server Role 'Hero', you should see a new channel 
category called "DUNGEON". This is where the game takes place. Only those 
members who are marked as the role 'Hero' can see or interact with these 
channels.

Basic game mechanics
---

### Locations (Discord channels)

A Location in the game corresponds to a Discord channel. Typing in a channel 
counts as interacting with that Location. One major Location in the game 
is __#town__, where various game events are announced and your messages 
can be interpreted as commands, like "score" to print out the current high scores 
(commands explained later). You can chat or role play in the channels, too, 
there is no restriction as to what you can type in. The other main Location 
is the __#wilderness__, which represents the area outside of town.

| Location  | Discord channel | Description |
| --- | --- | --- |
| Town | #town | Where quests are started, and game commands can be used. | 
| Wilderness | #wilderness | Where every message counts as 1 xp. Sometimes spawns enemies when on a Quest. | 

### Searching

The basic action of the game, any text typed in the __#wilderness__ channel 
will reward the player with 1 experience. The channel is often slowed to only 
allow one message per X seconds, to prevent spam.

### Discord Dungeon Master reactions

The Dungeon Master bot will respond to messages in the game.

| Emoji | Description |
| --- | --- |
| magnifying glass | The hero performed a search action and found nothing. |
| dash / gust | The hero tried to attack an enemy, and missed. |
| radiant star | The hero critically hit the enemy (see below for description on crits). |
| blood drop | The enemy hit the hero and that hero took 1 wound. |
| numbers 1 - 9 | The hero only has X hp left, where X is the emoji indicated. |
| skull and crossbones | An enemy got the last hit on a hero and they died. |

### Quests

Throughout the game, the Heroes will go on Quests, one at a time. Starting a 
quest can be down in __#town__ by typing `quest start`. This starts the next 
quest in the quest line, for the entire server (not just you, but all Heroes). 
You cannot start a quest if one is already started. To view the current quest, 
type `quest` in __#town__.

Once a quest is started the __#wilderness__ will be populated with a set of 
randomly generated enemies. From this point until the heroes complete the quest 
or it is abandoned, those typing into the __#wilderness__ have a chance to 
spawn one of the enemies.

When all the enemies in the area are slain, the area boss appears (if there is one).
Only when the boss is dead will the heroes complete the quest.

Once the quest is complete, all Heroes who landed at least one hit on an enemy 
during the quest's duration get the quest experience.

### Enemies

Enemies can spawn in the __#wilderness__ if a quest is active. An enemy has a 
set of hit points and reward experience if killed by the Heroes. Each 'wound' 
counts as a hit point. Once an enemy has 0 or fewer hit points, it is dead and 
all Heroes who landed at least one hit share the reward experience between them.

### Fighting

When an enemy spawns in the __#wilderness__, anything players type into the 
text channel after that is considered a 'fight' action.

A fight action can result in several things happening:

1. The hero missed the enemy.
2. The hero hit the enemy, wounding it by 1.
3. The hero managed a critical hit on the enemy, wounding it by an additional 1.
4. The enemy hit the hero, dealing 1 wound.
5. The enemy managed a critical hit on the hero, dealing 1 additional wound.
  
Enemies with an elemental type (see Elemental damage below) can also react 
according to their elemental weaknesses and strengths.

If the enemy dies, Heroes who landed at least one hit on the deceased enemy 
share in the enemy's reward experience.

#### Taking damage

Each time a Hero attacks an Enemy, the enemy gets an attack on that Hero. If the enemy hits, a wound will be dealt
to the hero, which is 1hp. A Hero starts with 

#### Elemental damage types

Along with normal Fighting attacks, certain elemental attacks may be used. Enemies
of a certain elemental type will be weak to another element.

![elemental damage weaknesses graph](https://i.imgur.com/tg6U9Qc.jpg "Elemental weaknesses. Each arrow is pointing to an element's weakness.")

Elemental attacks can be used by typing the element's emoji as your Fight action. If the game doesn't recognize
the element used a normal attack will be used instead.
