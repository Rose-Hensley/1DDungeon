from __future__ import annotations

from typing import List, Tuple, TYPE_CHECKING

from action import *

if TYPE_CHECKING:
    from actor import Actor
    from engine import Engine

class BaseAI:
    actor: Actor

    def perform(self, engine: Engine) -> float:
        raise NotImplementedError()


class SimpleMeleeHostileEnemy(BaseAI):
    def perform(self, engine: Engine) -> float:
        # if we are next to a hostile
        if engine.gamemap.get_adjacent_hostile(x=self.actor.x, y=self.actor.y) != None:
            BasicAttackAction(entity=self.actor).perform()
            return self.actor.fighter.base_speed

        # pathfind to player
        elif engine.player.x > self.actor.x:
            MovementAction(entity=self.actor, dx=1).perform()
            return self.actor.fighter.base_speed

        elif engine.player.x < self.actor.x:
            MovementAction(entity=self.actor, dx=-1).perform()
            return self.actor.fighter.base_speed

        else:
            WaitAction(entity=self.actor).perform()
            return self.actor.fighter.base_speed
