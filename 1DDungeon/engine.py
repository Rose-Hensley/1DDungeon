from __future__ import annotations

from typing import Iterable, Iterator, Optional, TYPE_CHECKING
import copy

from event_handler import EventHandler
from component import entity
from tcod.console import Console
from renderer import GameRenderer
from gamemap import GameMap
from include import constants
import entity_factory

class Engine:
    def __init__(self):
        self.event_handler: EventHandler = EventHandler(self)
        self.renderer_list = []
        self.player = copy.deepcopy(entity_factory.player)
        self.gamemap = GameMap(
            width=constants.gamemap_width,
            height=constants.gamemap_height,
            entities=[self.player],
            player=self.player
        )

        entity_factory.zombie.spawn(gamemap=self.gamemap, x=6, y=0)

        # starting the render list
        self.renderer_list.append(GameRenderer(self.gamemap))

    def render(self, console: Console) -> None:
        for renderer in self.renderer_list:
            renderer.render(console)

    def handle_enemy_turns(self) -> None:
        for entity in set(self.gamemap.actors) - {self.player}:
            if entity.ai:
                entity.ai.perform(self)
