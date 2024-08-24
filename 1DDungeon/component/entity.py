from __future__ import annotations

import copy

from typing import Optional, Tuple, Type, TypeVar, TYPE_CHECKING

from include.render_order import RenderOrder
from include import color

if TYPE_CHECKING:
    from gamemap import GameMap
    from component.fighter import Fighter

class Entity:
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = color.white,
        name: str = "<Unnamed>",
        blocks_movement: bool = False,
        render_order: RenderOrder = RenderOrder.CORPSE,
    ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement
        self.render_order = render_order

    def is_grabbable(self):
        return False

    def is_alive(self) -> bool:
        return False

    def move(self, dx: int, dy: int = 0) -> None:
        # Move the entity by a given amount
        self.x += dx
        self.y += dy

    def set_pos(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def spawn(self: T, gamemap: GameMap, x: int, y: int) -> T:
        """Spawn a copy of this instance at the given location."""
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        gamemap.entities.append(clone)
        return clone


# A type of entity with no AI that can be picked up
class PickupEntity(Entity):
    def is_grabbable(self) -> bool:
        return True

    def pickup(self, fighter: Fighter) -> None:
        raise NotImplementedError()


# A class that represents a gold pickup on the ground
class GoldPickup(PickupEntity):
    def __init__(
        self,
        x: int = 0,
        y: int = 0,
        char: str = "$",
        color: Tuple[int, int, int] = color.gold,
        name: str = "Gold",
        blocks_movement: bool = False,
        render_order: RenderOrder = RenderOrder.ITEM,
        gold_amount: int = 0,
    ):
        super().__init__(
            x=x, y=y, char=char,
            color=color, name=name,
            blocks_movement=blocks_movement,
            render_order=render_order,
        )
        self.gold_amount = gold_amount

    def pickup(self, fighter: Fighter) -> None:
        fighter.gold += self.gold_amount
