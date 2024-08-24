from __future__ import annotations

from tcod.console import Console

from gamemap import GameMap
from include import constants
from include import color
from component.entity import Entity

class Renderer:
    def render(self, console: Console) -> None:
        raise NotImplementedError()

    def render_bar(self,
        console: Console,
        x: int, y: int,
        curr_value: int,
        max_value: int,
        total_width: int,
        bar_fill: tuple[int, int, int],
        bar_empty: tuple[int, int, int],
        bar_text: tuple[int, int, int] = color.white,
        string: str = 'HP'
    ) -> None:
        bar_width = int(float(curr_value) / max_value * total_width) if max_value > 0 else 0

        console.draw_rect(x=x, y=y, width=total_width, height=1, ch=1, bg=bar_empty)

        if bar_width > 0:
            console.draw_rect(x=x, y=y, width=bar_width, height=1, ch=1, bg=bar_fill)

        console.print(x=x, y=y, string=f"{string}: {curr_value}/{max_value}", fg=bar_text)


    # draws the border around the given area
    # returns the top left point that you can draw things to
    def render_border(self, console: Console,
        x: int, y: int,
        width: int, height: int,
        decoration: str = '         ',
        fg: tuple[int, int, int] | None = None,
        bg: tuple[int, int, int] | None = None,
        title: str = ' ',
        title_color: tuple[int, int, int] | None = None,
    ) -> tuple[int, int]:
        if title_color == None:
            title_color = color.black
        console.print(x=x,y=y,string=title,fg=title_color,bg=bg)
        console.draw_frame(x=x, y=y+1, width=width, height=height, decoration=decoration, fg=fg, bg=bg)
        console.draw_rect(x=x+1,y=y+2,width=width-2,height=height-2,bg=color.black,ch=0)
        return (x+1, y+2)
        


class GameRenderer(Renderer):
    def __init__(self, gamemap: GameMap):
        self.gamemap = gamemap

    def render(self, console: Console) -> None:
        player_fighter = self.gamemap.player.fighter

        # finding the origin for border title
        game_map_x = constants.screen_width//2 - self.gamemap.width//2
        game_map_y = (constants.screen_height * 5) // 6

        # drawing gamemap border
        self.render_border(console,
            x=game_map_x,
            y=game_map_y,
            width=self.gamemap.width+2, height=self.gamemap.height+2,
            decoration='┌─┐│.│└─┘',
            title=f'{self.gamemap.name} {self.gamemap.floor}', title_color=color.white
        )

        # drawing targeted tiles
        for target_entity in self.gamemap.target_entities:
            console.print(
                x=game_map_x + target_entity.x + 1, y=game_map_y+self.gamemap.height+3,
                string='^', fg=color.white,
            )

        # drawing entities to the game map
        self.gamemap.entities = sorted(self.gamemap.entities, key=lambda x: x.render_order.value)
        for entity in self.gamemap.entities:
            console.print(
                x=entity.x + game_map_x+1, y=entity.y + game_map_y+2,
                string=entity.char, fg=entity.color
            )

        # Drawing character sheet
        # width and height of the drawable area on the sheet
        sheet_width, sheet_height = constants.screen_width//2 - 2, game_map_y-2
        sheet_x, sheet_y = self.render_border(console=console,
            x=0, y=0,
            width=sheet_width, height=sheet_height,
            bg=color.character_sheet_border, title=self.gamemap.player.name
        )

        # drawing hp bar
        self.render_bar(console=console, x=sheet_x+1,y=sheet_y+1,
            curr_value=player_fighter.hp, max_value=player_fighter.hp_max,
            total_width=sheet_width - 4,
            bar_fill=color.hp_bar_fill, bar_empty=color.hp_bar_empty, string='HP'
        )

        # drawing mp bar
        self.render_bar(console=console,
            curr_value=player_fighter.mp, max_value=player_fighter.mp_max,
            total_width=sheet_width - 4,
            x=sheet_x+1, y=sheet_y+3,
            bar_fill=color.mp_bar_fill, bar_empty=color.mp_bar_empty,string='MP'
        )

        # drawing xp bar
        self.render_bar(console=console,
            curr_value=player_fighter.xp, max_value=player_fighter.xp_to_next,
            total_width=sheet_width - 4,
            x=sheet_x+1, y=sheet_y+5,
            bar_fill=color.xp_bar_fill, bar_empty=color.xp_bar_empty, string='XP'
        )

        # drawing list of menus to navigate to
        console.print_box(x=sheet_x+1,y=sheet_y+7,
            width=sheet_width, height=sheet_height,
            string=f"""Bulk:{player_fighter.bulk}  Nimble:{player_fighter.nimble}  Magic:{player_fighter.magic}  Luck:{player_fighter.luck}

AC:{player_fighter.armor} EV:{player_fighter.evasion}

Gold:{player_fighter.gold}

f - Basic Attack (2d{player_fighter.basic_dmg})
TAB - Switch target""")


        if self.gamemap.target_entities:
            self.render_enemy_character_sheet(
                console=console, 
                entity=self.gamemap.target_entities[0],
                sheet_width=sheet_width, sheet_height=sheet_height,
            )

    def render_enemy_character_sheet(self, console: Console, entity: Entity, sheet_width: int, sheet_height: int):
        if entity != None and entity.is_alive():
            entity_fighter = entity.fighter
            sheet_x, sheet_y = self.render_border(console=console,
                x=constants.screen_width//2 + 1, y=0,
                width=sheet_width, height=sheet_height,
                bg=entity.color, title=entity.name
            )

            # drawing hp bar
            self.render_bar(console=console, x=sheet_x+1,y=sheet_y+1,
                curr_value=entity_fighter.hp, max_value=entity_fighter.hp_max,
                total_width=sheet_width - 4,
                bar_fill=color.hp_bar_fill, bar_empty=color.hp_bar_empty, string='HP'
            )

            # drawing mp bar
            self.render_bar(console=console,
                curr_value=entity_fighter.mp, max_value=entity_fighter.mp_max,
                total_width=sheet_width - 4,
                x=sheet_x+1, y=sheet_y+3,
                bar_fill=color.mp_bar_fill, bar_empty=color.mp_bar_empty,string='MP'
            )

            # drawing list of menus to navigate to
            console.print_box(x=sheet_x+1,y=sheet_y+7,
                width=sheet_width, height=sheet_height,
                string=f"""Blk:{entity_fighter.bulk} Cun:{entity_fighter.nimble} Mag:{entity_fighter.magic} Lck:{entity_fighter.luck}
AC:{entity_fighter.armor} EV:{entity_fighter.evasion}
Basic Attack (2d{entity_fighter.basic_dmg})""")


class GameOverRenderer(Renderer):
    def render(self, console: Console) -> None:
        width, height = 17, 7
        dialogue_x, dialogue_y = self.render_border(console=console,
            x=constants.screen_width//2 - 5, y=constants.screen_height//2 - 1,
            width=width, height=height,
            bg=color.white, title='GAME OVER'
        )
        console.print_box(x=dialogue_x,y=dialogue_y+1,
            width=width, height=height,
            string=""" ENTER - Reset

 ESC - Quit""")
