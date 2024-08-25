from __future__ import annotations

from typing import Optional, Tuple, TYPE_CHECKING
import random

from include import color

from component.inventory_item import WeaponItem
from component.entity import GoldPickup

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity
    

# Returns a delay to signify how long to action takes
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

        returns the amount of time it takes to complete the action

        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()


class EscapeAction(Action):
    def gives_up_turn(self) -> bool:
        return False

    def perform(self) -> None:
        print('Goodbye World')
        raise SystemExit()


class ResetGameAction(Action):
    def perform(self) -> None:
        Action.engine.reset_game()


class MovementAction(Action):
    def __init__(self, entity: Entity, dx: int, dy: int = 0):
        super().__init__(entity)
        self.dx = dx
        self.dy = dy

    def perform(self) -> None:
        if self.entity.x + self.dx == Action.engine.gamemap.width:
            MoveToNextLevelAction(self.entity).perform()
        elif not Action.engine.gamemap.inbounds(self.entity.x + self.dx, self.entity.y + self.dy):
            print('You walk into a wall')
        elif Action.engine.gamemap.block_at(self.entity.x + self.dx, self.entity.y + self.dy):
            print('Something blocks your path!')
        else:
            self.entity.move(self.dx, self.dy)

        EndTurnAction(self.entity).perform()


class MoveToNextLevelAction(Action):
    def gives_up_turn(self) -> bool:
        return False

    def perform(self) -> None:
        if not Action.engine.gamemap.in_combat():
            Action.engine.gamemap.generate_floor()


class WaitAction(Action):
    def perform(self) -> None:
        print(f'{self.entity.name} waits')
        EndTurnAction(self.entity).perform()


class GrabAction(Action):
    def gives_up_turn(self) -> bool:
        return False

    def perform(self) -> None:
        x_pos, y_pos = self.entity.x, self.entity.y
        for grabbable_entity in Action.engine.gamemap.entities:
            if grabbable_entity.is_grabbable() and grabbable_entity.x == x_pos and grabbable_entity.y == y_pos:
                grabbable_entity.pickup(self.entity.fighter)
                Action.engine.gamemap.entities.remove(grabbable_entity)


class DieAction(Action):
    def gives_up_turn(self) -> bool:
        return False

    def perform(self) -> None:
        if self.entity == Action.engine.player:
            Action.engine.game_over_state()
        else:
            # remove from targetted entities list if need be
            if self.entity in Action.engine.gamemap.target_entities:
                Action.engine.gamemap.target_entities.remove(self.entity)
                SwitchTargetAction(entity=self.entity).perform()

            # gain xp
            msg = Action.engine.player.gain_xp(xp=self.entity.fighter.xp)
            if msg != None:
                print(msg)

            # drop gold if carrying any
            if self.entity.fighter.gold > 0:
                Action.engine.gamemap.entities.append(
                    GoldPickup(
                        x=self.entity.x, y=self.entity.y, gold_amount=self.entity.fighter.gold
                    )
                )


class EndTurnAction(Action):
    def perform(self) -> None:
        self.entity.fighter.on_end_of_turn()


class SwitchTargetAction(Action):
    def gives_up_turn(self) -> bool:
        return False

    def perform(self) -> None:
        other_entities = sorted(Action.engine.gamemap.actors, key=lambda actor: actor.x)
        other_entities = list(filter(lambda actor: actor.hostile, other_entities))

        if not other_entities:
            Action.engine.gamemap.target_entities.clear()
            return

        if not Action.engine.gamemap.target_entities or Action.engine.gamemap.target_entities[0] not in other_entities:
            other_entity = other_entities[0]

        elif Action.engine.gamemap.target_entities:
            idx = other_entities.index(Action.engine.gamemap.target_entities[0])
            other_entity = other_entities[(idx+1) % len(other_entities)]

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
            #print(f'{self.entity.name} attacks {display_name} for {dmg}')

        EndTurnAction(self.entity).perform()


class WeaponAttack(Action):
    def __init__(self, entity: Entity, other_entities: list[Entity], weapon: WeaponItem) -> None:
        super().__init__(entity=entity)
        self.other_entities = other_entities
        self.weapon = weapon

    def perform(self) -> None:
        if not self.other_entities:
            print('No target to attack!')
            EndTurnAction(self.entity).perform()
            return

        for entity in self.other_entities:
            hit_roll = 100 - entity.fighter.evasion
            if abs(entity.x - self.entity.x) > self.weapon.target_range:
                print('Enemy outside of range!')

            elif random.randint(0, 99) >= hit_roll and entity.is_alive():
                self.weapon.on_miss(attacker=self.entity.fighter, target=entity.fighter)

            elif entity.is_alive():
                dmg_roll, dmg_type = self.weapon.get_damage_roll()
                entity.fighter.take_dmg(dmg_roll)
                self.weapon.on_hit(attacker=self.entity.fighter, target=entity.fighter)
                if not entity.is_alive():
                    self.weapon.on_kill(attacker=self.entity.fighter, target=entity.fighter)

            else:
                print('Attacking a not alive target')

        EndTurnAction(self.entity).perform()
