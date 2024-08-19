from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING

from include import color

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity
    

class Action:
    # Static engine variable that all action objects will share
    engine: Engine

    def __init__(self, entity: Entity) -> None:
        self.entity = entity

    def gives_up_turn(self) -> bool:
        return True

    def perform(self) -> None:
        """Perform this action with the objects needed to determine its scope.

        `Action.engine` is the scope this action is being performed in.

        `self.entity` is the object performing the action.

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class EscapeAction(Action):
    def perform(self) -> None:
        print('Goodbye World')
        raise SystemExit()


class MovementAction(Action):
    def __init__(self, entity: Entity, dx: int, dy: int = 0):
        super().__init__(entity)
        self.dx = dx
        self.dy = dy

    def perform(self) -> None:
        if not Action.engine.gamemap.inbounds(self.entity.x + self.dx, self.entity.y + self.dy):
            print('You walk into a wall')
        elif Action.engine.gamemap.block_at(self.entity.x + self.dx, self.entity.y + self.dy):
            print('Something blocks your path!')
        else:
            self.entity.move(self.dx, self.dy)

        EndTurnAction(self.entity).perform()


class WaitAction(Action):
    def perform(self) -> None:
        print(f'{self.entity.name} waits')
        EndTurnAction(self.entity).perform()


class DieAction(Action):
    def perform(self) -> None:
        if self.entity == Action.engine.player:
            Action.engine.game_over_state()
        else:
            msg = Action.engine.player.gain_xp(xp=self.entity.fighter.xp)
            if msg != None:
                print(msg)


class EndTurnAction(Action):
    def perform(self) -> None:
        self.entity.fighter.on_end_of_turn()


class SwitchTargetAction(Action):
    def gives_up_turn(self) -> bool:
        return False

    def perform(self) -> None:
        other_entity = next((enemy for enemy in Action.engine.gamemap.actors if enemy.hostile and \
            enemy not in Action.engine.gamemap.target_entities), None)
        Action.engine.gamemap.target_entities.clear()
        if other_entity != None:
            Action.engine.gamemap.target_entities.append(other_entity)


class BasicAttackAction(Action):
    def perform(self) -> None:
        target = Action.engine.gamemap.get_adjacent_hostile(x=self.entity.x, y=self.entity.y)
        if target == None:
            print('No enemies in range!')
        else:
            display_name = target.name
            dmg = self.entity.fighter.basic_attack(target)
            print(f'{self.entity.name} attacks {display_name} for {dmg}')

        EndTurnAction(self.entity).perform()