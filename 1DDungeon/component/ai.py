from __future__ import annotations

from typing import List, Tuple, TYPE_CHECKING

from action import *

if TYPE_CHECKING:
    from actor import Actor
    from engine import Engine

class BaseAI:
    actor: Actor

    def perform(self, engine: Engine) -> None:
        raise NotImplementedError()


class SimpleMeleeHostileEnemy(BaseAI):
    def perform(self, engine: Engine) -> None:
        # if we are next to a hostile
        if engine.gamemap.get_adjacent_hostile(x=self.actor.x, y=self.actor.y) != None:
            BasicAttackAction(self.actor, engine).perform()

        # pathfind to player
        elif engine.player.x > self.actor.x:
            MovementAction(self.actor, engine, dx=1).perform()

        elif engine.player.x < self.actor.x:
            MovementAction(self.actor, engine, dx=-1).perform()

        else:
            WaitAction(self.actor, engine).perform()
