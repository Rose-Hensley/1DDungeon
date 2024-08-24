from __future__ import annotations

from typing import TYPE_CHECKING

import random

from component.inventory_item import WeaponItem
from include.weapon_attributes import WeaponAttribute
from include.damage_types import DamageType

basic_bow = WeaponItem(name='Basic Bow',
    target_range=5,
    base_dmg=3,
    attributes=[
        WeaponAttribute.RANGED,
        WeaponAttribute.SWIFT,
        WeaponAttribute.TWO_HANDED,
    ],
    base_dmg_type=DamageType.SHARP
)

item_map = {
    1: basic_bow,

}
