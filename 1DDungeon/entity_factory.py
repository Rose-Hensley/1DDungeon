from __future__ import annotations

from typing import TYPE_CHECKING

import random

import item_factory
from component.actor import Actor
from component.ai import *
from component.fighter import Fighter
from component.player_fighter import PlayerFighter
from char_utils import *
from include import color

player = Actor(
    hostile=False,
    char='L',
    color=color.player_glyph,
    name='Liana LN-47',
    ai=BaseAI(),
    fighter=PlayerFighter(
        hp_max=30, mp_max=10,
        armor=1, evasion=10,
        hp_regen=1, mp_regen=1,
        basic_dmg=4, xp_to_next=2,
        bulk=2,nimble=4,magic=5,luck=4,
        weapon_equipped=item_factory.longbow.create_item(),
        base_speed=.5,
    ),
    
)

zombie = Actor(
    char='z',
    color=color.zombie_glyph,
    name='Zombie',
    ai=SimpleMeleeHostileEnemy(),
    fighter=Fighter(
        hp_max=random.randint(7,10),
        hp_regen=1, basic_dmg=3, xp=1, cr=1,
        base_speed=1,
    ),
)

zombie_carrier = Actor(
    char='Z',
    color=color.zombie_glyph,
    name='Zombie Carrier',
    ai=SimpleMeleeHostileEnemy(),
    fighter=Fighter(
        hp_max=random.randint(13,15),
        hp_regen=1, basic_dmg=4, xp=2, cr=2,
    ),
)

infected_survivor = Actor(
    char='I',
    color=color.infected_survivor_glyph,
    name='Infected Survivor',
    ai=SimpleMeleeHostileEnemy(),
    fighter=Fighter(
        hp_max=random.randint(18,20),
        hp_regen=1, basic_dmg=5, xp=3, cr=3,
        gold=random.randint(1,3),
    )
)

city_outskirts_enemies = [
    zombie,
    zombie_carrier,
    infected_survivor,
]
