from enum import Enum

class WeaponAttribute(Enum):
    # Weapon that requires two hands to use
    TWO_HANDED = 'Two-Handed'

    # Weapon that requires one hand
    ONE_HANDED = 'One-Handed'

    # Weapon which doesn't require an equipment other than the body
    UNNARMED = 'Unnarmed'

    # Weapon that can attack from a variable distance but does less up close
    RANGED = 'Ranged'

    # Weapon that can use Nimble for the damage
    SWIFT = 'Swift'

    # Weapon that can do melee attacks at 1-2 range
    POLEARM = 'Polearm'

    # Weapon that can be thrown and can use Bulk for damage
    THROWN = 'Thrown'
