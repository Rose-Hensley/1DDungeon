from __future__ import annotations

from typing import Optional, Tuple, Type, TypeVar, TYPE_CHECKING
import random
import copy

from include.weapon_attributes import WeaponAttribute
from include.damage_types import DamageType

if TYPE_CHECKING:
    from fighter import Fighter

# Class which represents an item in the inventory
#   uses: how many uses the item has before being destroyed. -1 for infinite use
class InventoryItem:
    def __init__(self,
        uses: int = -1,
        stackable: bool = False,
        count: int = 1,
        name: str = '<Unnamed>',
    ):
        self.uses = uses
        self.stackable = stackable
        self.count = count
        self.name = name

    def get_item_string(self) -> str:
        raise NotImplementedError()

    def create_item(self: T) -> T:
        clone = copy.deepcopy(self)
        return clone


class WeaponItem(InventoryItem):
    def __init__(self,
        uses: int = -1,
        stackable: bool = False,
        count: int = 1,
        name: str = '<Unnamed>',
        target_range: int = 1,
        base_dmg: int = 0,
        base_dmg_type: DamageType = DamageType.SHARP,
        attributes: list[WeaponAttribute] = [],
    ):
        super().__init__(uses=uses, stackable=stackable, count=count, name=name)
        self.target_range = target_range
        self.base_dmg = base_dmg
        self.base_dmg_type = base_dmg_type
        self.attributes = attributes

    def get_item_string(self) -> str:
        pass

    def get_damage_roll(self) -> (int, DamageTypes):
        if self.base_dmg > 1:
            return random.randint(1,self.base_dmg) + random.randint(1,self.base_dmg), self.base_dmg_type
        else:
            return self.base_dmg * 2, self.base_dmg_type

    def on_hit(self, attacker: Fighter, target: Fighter) -> None:
        pass

    def on_kill(self, attacker: Fighter, target: Fighter) -> None:
        pass

    def on_dodge(self, attacker: Fighter, target: Fighter) -> None:
        pass

    def on_miss(self, attacker: Fighter, target: Fighter) -> None:
        pass
