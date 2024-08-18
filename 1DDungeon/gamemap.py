from __future__ import annotations

from typing import Iterable, Iterator, Optional, TYPE_CHECKING

class GameMap:
    def __init__(self, player: Actor, width: int, height: int = 1, entities: Iterable[Entity] = ()):
        self._width, self._height = width, height
        self.entities = set(entities)
        self.player = player

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

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
    def actors(self) -> Iterator[Actor]:
        """Iterate over this maps living actors."""
        yield from (entity for entity in self.entities if entity.is_alive)

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
