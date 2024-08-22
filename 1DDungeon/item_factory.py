from __future__ import annotations

from typing import TYPE_CHECKING

import random

from component.inventory_item import WeaponItem
from include.weapon_attributes import WeaponAttributes

basic_bow = WeaponItem(name='Basic Bow', target_range=5, base_dmg=5, attributes=[
    WeaponAttributes.RANGED,
    WeaponAttributes.SWIFT,
    WeaponAttributes.TWO_HANDED,
    ]
)
