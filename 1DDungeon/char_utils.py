from tcod import tileset

def get_character(x: int, y: int) -> str:
    return chr(tileset.CHARMAP_CP437[x + 16*y])
