from __future__ import annotations

from typing import TYPE_CHECKING

import random

from component.actor import Actor
from component.ai import *
from component.fighter import Fighter
from component.player_fighter import PlayerFighter
from char_utils import *
from include import color

player = Actor(
    hostile=False,
    char=get_character(12,0),
    color=color.player_glyph,
    name='Marisa',
    ai=BaseAI(),
    fighter=PlayerFighter(
        hp_max=30, mp_max=10,
        armor=1, evasion=10,
        hp_regen=1, mp_regen=1,
        basic_dmg=4, xp_to_next=2,
        bulk=3,cunning=4,magic=5,luck=4
    ),
)

zombie = Actor(
    char='z',
    color=color.zombie_glyph,
    name='Zombie',
    ai=SimpleMeleeHostileEnemy(),
    fighter=Fighter(
        hp_max=random.randint(7,10),
        hp_regen=1, basic_dmg=3, xp=1,
    ),
)

zombie_carrier = Actor(
    char='Z',
    color=color.zombie_glyph,
    name='Zombie Carrier',
    ai=SimpleMeleeHostileEnemy(),
    fighter=Fighter(
        hp_max=random.randint(13,15),
        hp_regen=1, basic_dmg=4, xp=2,
    ),
)
