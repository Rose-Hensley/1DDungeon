from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import tcod.event
from tcod import context
from action import *

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

WAIT_KEYS = [
    tcod.event.KeySym.s,
]

ATTACK_KEYS = [
    tcod.event.KeySym.f,
]

SWITCH_TARGET_KEYS = [
    tcod.event.KeySym.TAB
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
            action.perform()

            print(self.engine.gamemap.target_entities)

            if action.gives_up_turn():
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

        # No valid key was pressed
        return action


class GameOverHandler(EventHandler):
    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Action]:
        action: Optional[Action] = None

        key = event.sym
        player = self.engine.player

        if key in QUIT_KEYS:
            action = EscapeAction(entity=player)

        # No valid key was pressed
        return action
