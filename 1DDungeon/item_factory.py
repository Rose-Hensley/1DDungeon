from __future__ import annotations

from typing import TYPE_CHECKING

import random

from component.inventory_item import WeaponItem
from include.weapon_attributes import WeaponAttribute
from include.damage_types import DamageType

longbow = WeaponItem(name='Longbow',
    target_range=8,
    base_dmg=3,
    attributes=[
        WeaponAttribute.RANGED,
        WeaponAttribute.SWIFT,
        WeaponAttribute.TWO_HANDED,
    ],
    base_dmg_type=DamageType.SHARP,
    base_speed=1.1,
)

shortbow = WeaponItem(name='Longbow',
    target_range=6,
    base_dmg=3,
    attributes=[
        WeaponAttribute.RANGED,
        WeaponAttribute.SWIFT,
        WeaponAttribute.TWO_HANDED,
    ],
    base_dmg_type=DamageType.SHARP,
    base_speed=0.95,
)

item_map = {
    1: longbow,
    2: shortbow,

}
