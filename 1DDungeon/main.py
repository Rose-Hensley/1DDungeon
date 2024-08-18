import tcod

from action import EscapeAction, MovementAction
from event_handler import EventHandler
from engine import Engine
from include import constants

def main():
    tileset = tcod.tileset.load_tilesheet("./assets/tileset.png", 16, 16, tcod.tileset.CHARMAP_CP437)

    engine = Engine()

    with tcod.context.new_terminal(
            constants.screen_width,
            constants.screen_height,
            tileset=tileset,
            title="1DDungeon",
            vsync=True,
        ) as context:
            root_console = tcod.console.Console(constants.screen_width, constants.screen_height, order="F")
            while True:
                root_console.clear()
                engine.render(console=root_console)

                context.present(root_console)

                engine.event_handler.handle_events(context)


if __name__ == "__main__":
    main()
