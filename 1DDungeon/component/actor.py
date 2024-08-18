from __future__ import annotations

from typing import Optional, Tuple, Type, TypeVar, TYPE_CHECKING

from component.ai import BaseAI
from component.fighter import Fighter
from component.entity import *

class Actor(Entity):
    def __init__(
        self,
        *,
        x: int = 0,
        y: int = 0,
        char: str = "?",
        color: Tuple[int, int, int] = (255, 255, 255),
        name: str = "<Unnamed>",
        ai: BaseAI = None,
        fighter: Fighter = None,
        hostile: bool = True
    ):
        super().__init__(
            x=x,
            y=y,
            char=char,
            color=color,
            name=name,
            blocks_movement=True,
        )
        self.ai = ai
        self.ai.actor = self
        self.fighter = fighter
        self.fighter.actor = self
        self.hostile = hostile

    def is_alive(self) -> bool:
        return self.fighter.hp > 0

    def die(self) -> None:
        print(f'{self.name} died!')
        self.char = "%"
        self.blocks_movement = False
        self.ai = None
        self.name = f"remains of {self.name}"
