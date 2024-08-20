from __future__ import annotations

from typing import Iterable, Iterator, Optional, TYPE_CHECKING
import copy

from action import Action
from event_handler import EventHandler, MainGameHandler, GameOverHandler
from component import entity
from tcod.console import Console
from renderer import GameRenderer, GameOverRenderer
from gamemap import GameMap
from include import constants
import entity_factory

class Engine:
    def __init__(self):
        self.event_handler: EventHandler = MainGameHandler(self)
        self.renderer_list = []
        self.player = copy.deepcopy(entity_factory.player)
        self.gamemap = GameMap(
            width=constants.gamemap_width,
            height=constants.gamemap_height,
            entities=[self.player],
            player=self.player
        )

    def engine_init(self):
        # Setting action engine to this
        Action.engine = self

        # starting the render list
        self.renderer_list.append(GameRenderer(self.gamemap))

        entity_factory.zombie_carrier.spawn(gamemap=self.gamemap, x=10, y=0)
        entity_factory.zombie.spawn(gamemap=self.gamemap, x=5, y=0)
        entity_factory.zombie.spawn(gamemap=self.gamemap, x=7, y=0)
        self.gamemap.entities.append(entity.GoldPickup(x=3, y=0, gold_amount=15))

    def reset_game(self):
        self.renderer_list = []
        self.event_handler = MainGameHandler(self)
        self.player = copy.deepcopy(entity_factory.player)
        self.gamemap = GameMap(
            width=constants.gamemap_width,
            height=constants.gamemap_height,
            entities=[self.player],
            player=self.player
        )

        self.engine_init()

    def render(self, console: Console) -> None:
        for renderer in self.renderer_list:
            renderer.render(console)

    def handle_enemy_turns(self) -> None:
        for entity in set(self.gamemap.actors) - {self.player}:
            if entity.ai:
                entity.ai.perform(self)

    def game_over_state(self) -> None:
        self.event_handler = GameOverHandler(engine=self)
        self.renderer_list.append(GameOverRenderer())
