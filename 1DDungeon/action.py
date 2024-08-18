from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING

from include import color

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

class Action:
    def __init__(self, entity: Entity, engine: Engine) -> None:
        super().__init__()
        self.entity = entity
        self.engine = engine

    def perform(self) -> None:
        """Perform this action with the objects needed to determine its scope.

        `self.engine` is the scope this action is being performed in.

        `self.entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class EscapeAction(Action):
    def perform(self) -> None:
        print('Goodbye World')
        raise SystemExit()


class MovementAction(Action):
    def __init__(self, entity: Entity, engine: Enginge, dx: int, dy: int = 0):
        super().__init__(entity, engine)
        self.dx = dx
        self.dy = dy

    def perform(self) -> None:
        if not self.engine.gamemap.inbounds(self.entity.x + self.dx, self.entity.y + self.dy):
            print('You walk into a wall')
        elif self.engine.gamemap.block_at(self.entity.x + self.dx, self.entity.y + self.dy):
            print('Something blocks your path!')
        else:
            self.entity.move(self.dx, self.dy)
            print('Move')

class WaitAction(Action):
    def perform(self) -> None:
        print('Wait')
        pass

class BasicAttackAction(Action):
    def perform(self) -> None:
        target = self.engine.gamemap.get_adjacent_hostile(x=self.entity.x, y=self.entity.y)
        if target == None:
            print('No enemies in range!')
        else:
            display_name = target.name
            dmg = self.entity.fighter.basic_attack(target)
            print(f'{self.entity.name} attacks {display_name} for {dmg}')
