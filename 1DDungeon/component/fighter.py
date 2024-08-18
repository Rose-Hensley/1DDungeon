from __future__ import annotations

from typing import TYPE_CHECKING

import random

from include import constants

if TYPE_CHECKING:
    from entity import Actor

class Fighter:

    actor: Actor

    def __init__(
        self,
        hp_max: int = 0, hp: int | None = None, 
        mp_max: int = 0, mp: int | None = None, 
        xp: int = 0, xp_to_next: int = 0,
        armor: int = 0, evasion: int = 0,
        bulk: int = 0, cunning: int = 0, magic: int = 0, luck: int = 0,
        hp_regen: int = 0, mp_regen: int = 0,
        basic_dmg: int = 0, level: int = 1,
    ):
        self.hp = hp_max if hp == None else hp
        self.hp_max = hp_max
        self.mp = mp_max if mp == None else mp
        self.mp_max = mp_max
        self.xp = xp
        self.xp_to_next = xp_to_next
        self.armor = armor
        self.evasion = evasion
        self.hp_regen = hp_regen
        self.mp_regen = mp_regen
        self.basic_dmg = basic_dmg
        self.bulk = bulk
        self.cunning = cunning
        self.magic = magic
        self.luck = luck

    # returns the actual amount of damage taken
    def take_dmg(self, dmg: int) -> int:
        # apply armor first
        reduction = 0
        if self.armor > 0:
            reduction = random.randint(0,self.armor) + random.randint(0,self.armor)
        dmg = max(0, dmg - reduction)
        self.hp = max(0, self.hp - dmg)
        if self.hp == 0:
            self.actor.die()
        return dmg

    # does damage equal to '2 dice <basic_dmg>'
    # returns amount of damage dealt
    def basic_attack(self,other_actor: Actor) -> int:
        if self.basic_dmg > 1:
            return other_actor.fighter.take_dmg(random.randint(1,self.basic_dmg) + random.randint(1,self.basic_dmg))
        else:
            return other_actor.fighter.take_dmg(self.basic_dmg * 2)

    # returns the actual amount of hp gained
    def gain_hp(self, hp: int) -> int:
        if self.hp + hp > self.hp_max:
            ret = self.hp + hp - self.hp_max
            self.hp = self.hp_max
            return ret
        else:
            self.hp += hp
            return hp

    # returns the actual amount of mp gained
    def gain_mp(self, mp:int) -> int:
        if self.mp + mp > self.mp_max:
            ret = self.mp + mp - self.mp_max
            self.mp = self.mp_max
            return ret
        else:
            self.mp += mp
            return mp

    # returns a message about you leveling up or None if no level up happened
    def gain_xp(self, xp:int) -> str | None:
        self.xp += xp
        if self.xp >= self.xp_to_next:
            self.xp -= self.xp_to_next
            return self.level_up()
        else:
            return None

    # returns a message about you leveling up or None if no level up happened
    def level_up(self) -> str | None:
        self.xp_to_next += constants.xp_to_next_increment
        return f'{self.actor.name} levels up!'

    def on_end_of_turn(self) -> None:
        if self.actor.is_alive():
            self.gain_hp(hp=self.hp_regen)
            self.gain_mp(mp=self.mp_regen)
