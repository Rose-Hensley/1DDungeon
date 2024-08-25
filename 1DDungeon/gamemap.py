from __future__ import annotations

from typing import Iterable, Iterator, Optional, TYPE_CHECKING
from random import shuffle

from include import constants
import entity_factory

if TYPE_CHECKING:
    from component.entity import Entity

class GameMap:
    def __init__(self,
        player: Actor,
        width: int,
        height: int = 1,
        name: str = '<Unnamed>',
        floor: int = 0,
        map_cr: int = 0,
        entities: Iterable[Entity] = [],
        target_tiles: list[Entity] = [],
    ):
        self._width, self._height = width, height
        self.entities = entities
        self.player = player
        self.name = name
        self.floor = floor
        self.target_entities = []
        self.map_cr = map_cr
        self.init_gamemap()

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def generate_floor(self) -> None:
        raise NotImplementedError()

    def _generate_floor_helper(self, spawnable_entities: list[Entity]) -> None:
        # Resetting the entities list
        self.entities.clear()
        self.entities.append(self.player)
        self.player.set_pos(0,0)

        # Incrementing floor and calculating cr rating for the level
        self.floor += 1
        max_cr = self.map_cr + int(self.floor / 2)

        # Choosin enemies
        curr_cr = max_cr
        shuffle(spawnable_entities)
        sorted_enemies = sorted(
            spawnable_entities,
            key=lambda e: e.fighter.cr,
            reverse=True
        )
        placed = True
        available_spaces = [i for i in range(3, self.width)]
        while(placed):
            placed = False
            for enemy in sorted_enemies:
                if enemy.fighter.cr <= curr_cr and available_spaces:
                    placed = True
                    curr_cr -= enemy.fighter.cr
                    print(available_spaces)
                    shuffle(available_spaces)
                    enemy.spawn(gamemap=self,x=available_spaces.pop(),y=0)
                    print(available_spaces)

    def init_gamemap(self):
        raise NotImplementedError()

    # returns whether the given space is in bounds or not
    def inbounds(self, x: int, y: int) -> bool:
        return x >= 0 and x < self.width and y >= 0 and y < self.height

    # returns a list of entities at given location
    def entities_at(self, x:int, y:int) -> list[Entity]:
        return [entity for entity in self.entities if entity.x == x and entity.y == y]

    # returns whether there is a blocker at the location or not
    def block_at(self, x:int, y:int) -> bool:
        return any([entity.blocks_movement for entity in self.entities_at(x=x,y=y)])

    @property
    def actors(self) -> List[Actor]:
        """Iterate over this maps living actors."""
        return [entity for entity in self.entities if entity.is_alive()]

    def get_actor_at_location(self, x: int, y: int = 0) -> Optional[Actor]:
        for actor in self.actors:
            if actor.x == x and actor.y == y:
                return actor
        return None

    def get_adjacent_hostile(self, x:int, y:int=0) -> Optional[Actor]:
        for actor in self.actors:
            if abs(actor.x - x) > 1 or abs(actor.y - y) > 1 \
                or self.get_actor_at_location(x=x,y=y).hostile == actor.hostile or not actor.is_alive():
                continue
            else:
                return actor
        return None

    def in_combat(self) -> bool:
        for a in self.actors:
            if a.is_alive() and a.hostile:
                return True
        return False



class CityOutskirtsMap(GameMap):
    def init_gamemap(self):
        self.name = 'City Outskirts'
        self.map_cr = constants.city_outskirt_cr

    # Increments the floor level by one each call
    def generate_floor(self):
        self._generate_floor_helper(entity_factory.city_outskirts_enemies)
