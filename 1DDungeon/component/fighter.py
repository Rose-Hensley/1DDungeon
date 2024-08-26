from __future__ import annotations

from typing import TYPE_CHECKING

import random

from component.inventory_item import WeaponItem
from include import constants

if TYPE_CHECKING:
    from entity import Actor
    

class Fighter:

    actor: Actor

    def __init__(
        self,
        hp_max: int = 0, hp: int | None = None, 
        mp_max: int = 0, mp: int | None = None, 
        xp: int = 0,
        armor: int = 0, evasion: int = 0,
        bulk: int = 0, nimble: int = 0, magic: int = 0, luck: int = 0,
        hp_regen: int = 0, mp_regen: int = 0,
        basic_dmg: int = 0, 
        weapon_equipped: WeaponItem | None = None,
        gold: int = 0,
        cr: int = 0,
        time_counter: float = 0.01,
        base_speed: float = 1.00,
    ):
        self.hp = hp_max if hp == None else hp
        self.hp_max = hp_max
        self.mp = mp_max if mp == None else mp
        self.mp_max = mp_max
        self.xp = xp
        self.armor = armor
        self.evasion = evasion
        self.hp_regen = hp_regen
        self.mp_regen = mp_regen
        self.basic_dmg = basic_dmg
        self.bulk = bulk
        self.nimble = nimble
        self.magic = magic
        self.luck = luck
        self.gold = gold
        self.weapon_equipped = weapon_equipped
        self.cr = cr
        self.time_counter = time_counter
        self.base_speed = base_speed

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
        if random.randint(1,100) > other_actor.fighter.evasion:
            if self.basic_dmg > 1:
                return other_actor.fighter.take_dmg(random.randint(1,self.basic_dmg) + random.randint(1,self.basic_dmg))
            else:
                return other_actor.fighter.take_dmg(self.basic_dmg * 2)
        else:
            print(f'{other_actor.name} dodges the attack!')
            return 0

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

    def on_end_of_turn(self) -> None:
        if self.actor.is_alive():
            self.gain_hp(hp=self.hp_regen)
            self.gain_mp(mp=self.mp_regen)

    def reset_time_counter(self) -> None:
        self.time_counter = 0.0

    # Returns the amount of time taken to attack with the equipped weapon otherwise base_speed
    def get_weapon_time(self) -> float:
        if self.weapon_equipped == None:
            return self.base_speed
        return max(
            self.weapon_equipped.max_speed,
            self.weapon_equipped.base_speed - self.weapon_equipped.base_speed * constants.speed_decrease_each_point * (self.nimble + self.bulk)
        )
