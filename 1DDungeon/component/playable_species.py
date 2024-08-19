from __future__ import annotations

from typing import List, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from player_fighter import PlayerFighter

class Species:
    player_fighter: PlayerFighter

    def __init__(self, species_id):
        self.species_id = species_id
        self.hp_mod = 5
