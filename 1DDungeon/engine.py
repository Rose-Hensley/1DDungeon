from __future__ import annotations

from typing import Iterable, Iterator, Optional, TYPE_CHECKING
import copy

from action import Action
from event_handler import EventHandler, MainGameHandler, GameOverHandler
from component import entity
from tcod.console import Console
from renderer import GameRenderer, GameOverRenderer
from gamemap import CityOutskirtsMap
from include import constants
import entity_factory

class Engine:
    def __init__(self):
        self.event_handler: EventHandler = MainGameHandler(self)
        self.renderer_list = []
        self.player = copy.deepcopy(entity_factory.player)
        self.gamemap = CityOutskirtsMap(
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

        # starting the first level
        self.gamemap.generate_floor()

        self.gamemap.entities.append(entity.GoldPickup(x=3, y=0, gold_amount=15))

    def reset_game(self):
        self.renderer_list = []
        self.event_handler = MainGameHandler(self)
        self.player = copy.deepcopy(entity_factory.player)
        self.gamemap = CityOutskirtsMap(
            width=constants.gamemap_width,
            height=constants.gamemap_height,
            entities=[self.player],
            player=self.player
        )

        self.engine_init()

    """
    def game_tick(self, console: Console, context: ) -> None:
        self.render(console=console)
        next_entity = self.engine.gamemap.get_next_turn_entity()
        if next_entity == self.player:
            self.event_handler.handle_events()
        else:
            self.handle_enemy_turn(entity=next_entity)
    """

    def render(self, console: Console) -> None:
        for renderer in self.renderer_list:
            renderer.render(console)

    def handle_enemy_turns(self) -> None:
        """
        for entity in set(self.gamemap.actors) - {self.player}:
            if entity.ai:
                time_used = entity.ai.perform(self)
                entity.increment_time_counter(time_used)"""

        while(self.gamemap.in_combat() and (next_entity := self.gamemap.get_next_turn_entity()) != self.player):
            time_used = self.handle_enemy_turn(next_entity)
            next_entity.increment_time_counter(time_used)

    def handle_enemy_turn(self, entitiy: entity.Entity) -> float:
        if entitiy.ai:
            return entitiy.ai.perform(self)

    def game_over_state(self) -> None:
        self.event_handler = GameOverHandler(engine=self)
        self.renderer_list.append(GameOverRenderer())
