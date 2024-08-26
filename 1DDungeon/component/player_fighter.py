from __future__ import annotations

from typing import List, Tuple, TYPE_CHECKING

from component.fighter import Fighter
from component.playable_species import Species
from include import constants
from component.inventory_item import WeaponItem

if TYPE_CHECKING:
    from inventory_item import InventoryItem

# Player fighter who is able to level up and has an inventory
class PlayerFighter(Fighter):
    def __init__(
        self,
        hp_max: int = 0, hp: int | None = None, 
        mp_max: int = 0, mp: int | None = None, 
        xp: int = 0, xp_to_next: int = 0,
        armor: int = 0, evasion: int = 0,
        bulk: int = 0, nimble: int = 0, magic: int = 0, luck: int = 0,
        hp_regen: int = 0, mp_regen: int = 0,
        basic_dmg: int = 0, level: int = 1,
        base_speed: float = 1.0,
        species: Species = Species(0),
        inventory: List[InventoryItem] = [],
        weapon_equipped: WeaponItem | None = None,
    ):
        super().__init__(
            hp_max=hp_max, hp=hp,
            mp_max=mp_max, mp=mp,
            xp=xp,
            armor=armor, evasion=evasion,
            bulk=bulk, nimble=nimble, magic=magic, luck=luck,
            hp_regen=hp_regen, mp_regen=mp_regen,
            basic_dmg=basic_dmg, base_speed=base_speed,
            weapon_equipped=weapon_equipped,
        )
        self.xp_to_next = xp_to_next
        self.level = level
        self.species = species
        self.species.player_fighter = self
        self.update_stat_calculations()

    # sets hp_max and evasion by the stat calculations provided
    def update_stat_calculations(self):
        # Calcing hp max and setting hp if necessary
        self.hp_max = self.level * 4 + self.bulk * 2 + self.species.hp_mod
        self.hp = self.hp_max if self.hp > self.hp_max else self.hp

        # Calcing evasion
        self.evasion = self.nimble * 3 + self.luck * 3

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
        self.level += 1
        return f'{self.actor.name} is now level {self.level}!'
