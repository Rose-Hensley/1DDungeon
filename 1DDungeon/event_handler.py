from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import tcod.event
from tcod import context
from action import *

import item_factory

if TYPE_CHECKING:
    from engine import Engine
    

MOVE_KEYS = {
    tcod.event.KeySym.LEFT: -1,
    tcod.event.KeySym.RIGHT: 1,
    tcod.event.KeySym.a: -1,
    tcod.event.KeySym.d: 1,
}

QUIT_KEYS = [
    tcod.event.KeySym.ESCAPE,
]

CONFIRM_KEYS = [
    tcod.event.KeySym.RETURN,
]

GRAB_KEYS = [
    tcod.event.KeySym.g,
]

WAIT_KEYS = [
    tcod.event.KeySym.s,
]

ATTACK_KEYS = [
    tcod.event.KeySym.f,
]

SWITCH_TARGET_KEYS = [
    tcod.event.KeySym.TAB
]

SHOOT_KEYS = [
    tcod.event.KeySym.w
]


class EventHandler(tcod.event.EventDispatch[Action]):
    def __init__(self, engine: Engine):
        self.engine = engine

    def handle_events(self, context: tcod.context.Context) -> None:
        for event in tcod.event.wait():
            context.convert_event(event)
            action = self.dispatch(event)
            if action is None:
                continue
            action.perform()

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Action]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        raise NotImplementedError()


class MainGameHandler(EventHandler):
    def handle_events(self, context: tcod.context.Context) -> None:
        for event in tcod.event.wait():
            context.convert_event(event)
            action = self.dispatch(event)
            if action is None:
                continue
            
            time_used = action.perform()
            action.entity.increment_time_counter(time=time_used)

            self.engine.handle_enemy_turns()


    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym
        player = self.engine.player

        if key in MOVE_KEYS:
            action = MovementAction(entity=player, dx=MOVE_KEYS[key])

        elif key in QUIT_KEYS:
           action = EscapeAction(entity=player)

        elif key in WAIT_KEYS:
            action = WaitAction(entity=player)

        elif key in ATTACK_KEYS:
            action = BasicAttackAction(entity=player)

        elif key in SWITCH_TARGET_KEYS:
            action = SwitchTargetAction(entity=player)

        elif key in GRAB_KEYS:
            action = GrabAction(entity=player)

        elif key in SHOOT_KEYS:
            action = WeaponAttack(
                entity=player,
                other_entities=self.engine.gamemap.target_entities,
                weapon=player.fighter.weapon_equipped
            )

        # No valid key was pressed
        return action


class GameOverHandler(EventHandler):
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym
        player = self.engine.player

        if key in QUIT_KEYS:
            action = EscapeAction(entity=player)

        elif key in CONFIRM_KEYS:
            action = ResetGameAction(entity=player)

        # No valid key was pressed
        return action
