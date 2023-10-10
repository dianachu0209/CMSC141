"""
Reversi Game GUI using Pygame
"""
import os
import sys
from typing import List, Tuple, Dict, Optional

import pygame
import pygame.font
import click
from reversi import Reversi

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


pygame.mixer.init()
pygame.mixer.music.load("media/reversi_music.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)



BLACK = (0, 0, 0)
GHOST_BLACK = (120, 120, 120)
WHITE = (255, 255, 255)
GHOST_WHITE = (220, 220, 220)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
VIOLET = (143, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BROWN = (100, 69, 19)
ORANGE = (255, 165, 0)
GHOST_RED = (155, 100, 100)
GHOST_BLUE = (150, 150, 255)
GHOST_VIOLET = (180, 150, 200)
GHOST_YELLOW = (200, 190, 150)
GHOST_GREEN = (100, 150, 100)
GHOST_BROWN = (150, 120, 90)
GHOST_ORANGE = (200, 130, 70)


color_dict: Dict[Optional[int], Tuple[Tuple[int, int, int], Tuple[int, int,\
    int]]] = {1: (BLACK, GHOST_BLACK)
            , 2: (WHITE, GHOST_WHITE),3: (RED, GHOST_RED), 4: (BLUE, GHOST_BLUE)
            ,5: (VIOLET, GHOST_VIOLET), 6: (YELLOW, GHOST_YELLOW), 7: (GREEN,\
                GHOST_GREEN), 8 : (BROWN, GHOST_BROWN), 9: (ORANGE,\
                    GHOST_ORANGE)}
fonts = pygame.font.get_fonts()

class Circle(pygame.sprite.Sprite):
    """
    Class to represent a circle object, inheriting from
    pygame sprite class.
    """
    def __init__(self, color, position, radius):
        super().__init__()
        self.color: Tuple[int, int, int] = color
        self.radius: int = radius
        self.image: pygame.Surface = pygame.Surface((2*self.radius,\
            2*self.radius), pygame.SRCALPHA)
        self.rect: pygame.rect = self.image.get_rect(center=position)

    def draw(self, surface):
        """
        Method for drawing a circle given a target surface,
        color, center, and radius
        
        Returns:
            Nothing
        """
        pygame.draw.circle(surface, self.color, self.rect.center, self.radius)

# Create a sprite group
circle_group: pygame.sprite.Group = pygame.sprite.Group()

class ReversiGui:
    """
    Class for a GUI-based Reversi board game.
    """

    window : int
    border : int
    surface : pygame.surface.Surface
    clock : pygame.time.Clock

    def __init__(self, board_size: int = 8, window: int = 600, border: int = 40,
                 num_of_plays: int = 2, othello: bool = True):
        """
        Constructor

        Parameters:
            window : int : height of window
            border : int : number of pixels to use as border around elements
            board_size : int : number of squares on each side of board.
            num_of_plays : int : number of players in the game.
            othello: bool : True if board starts with four pieces in the center.
            
        """
        self.game_surface = pygame.surface.Surface((window, window))
        self.game_surface.set_colorkey((0, 0, 0))
        self.window = window
        self.border = border
        self.game = Reversi(board_size, num_of_plays, othello)
        self.status : Dict = {}
        for i in range(1, num_of_plays + 1):
            self.status[i] = self.game.turn == i
        self.recs_in_grid: List[List[Optional[ReversiRect]]] = [[None] *\
            board_size for _ in range(board_size)]
        self.start = False
        self.rect_button = pygame.Rect(224, 400, 200, 50)
        self.start_button_status = False
        self.highlight_square = None


        # Initialize Pygame
        pygame.init()
        # Set window title
        pygame.display.set_caption("Reversi")


        # Set window size
        self.surface = pygame.display.set_mode((window + border + board_size,
                                                window))
        self.clock = pygame.time.Clock()
        self.last_input_time = pygame.time.get_ticks()
        self.render_delay_threshold = 500
        self.mouse_move = False

        self.event_loop()

    def draw_window(self) -> None:
        """
        Draws the contents of the window

        Parameters: none beyond self

        Returns: nothing
        """
        pygame.font.init()
        self.game_surface.fill((0, 0, 0))
        cells_side = len(self.game.grid)
        font_player = pygame.font.SysFont("Arial", 14)
        font = pygame.font.SysFont("Arial", 24)
        if not self.start:
            square = (self.window - 2 * self.border) // (15)
            start_text_surface = font.render("LET'S PLAY REVERSI!", True,\
                (WHITE))
            start_text_position = (210, 100)
            self.surface.fill((139, 69, 19))
            self.surface.blit(start_text_surface, start_text_position)
            info_text_surface = font.render\
                (f"{self.game.num_players} Player Game",True, (WHITE))
            info_text_position = (250, 300)
            self.surface.blit(info_text_surface, info_text_position)
            pygame.draw.rect(self.surface, WHITE, self.rect_button)
            if self.start_button_status:
                pygame.draw.rect(self.surface, YELLOW, self.rect_button, 10)
            button_text_surface = font.render("Start!", True, BLACK)
            button_text_position = (self.rect_button.x + 70, self.rect_button.y\
                + 10)
            self.surface.blit(button_text_surface, button_text_position)
            for i in range(1, self.game.num_players + 1):
                color = color_dict[i][0]
                position = ((i) * square + 4 * self.border +\
                    (9 -self.game.num_players ) * square //2, 250)
                radius = square
                circle = Circle(color, position, radius)
                circle_group.add(circle)
            for circle in circle_group:
                circle.draw(self.surface)
        else:
            if self.game.done:
                print(self.game.outcome)
                self.surface.fill((0, 0, 0))
                if len(self.game.outcome) != 1:
                    for i, player in enumerate(self.game.outcome):
                        end_text_surface = font.render\
                            (f"Player {player}", True, \
                                WHITE)
                        text_position = (100, 100 + i*30)
                        self.surface.blit(end_text_surface, text_position)
                    draw_message = font.render("Tied!", True, WHITE)
                    draw_message_pos = (200, 100)
                    self.surface.blit(draw_message, draw_message_pos)
                else:
                    turn1 = self.game.outcome[0]
                    end_text_surface = font.render\
                        (f"Player {turn1} wins! Please exit the window.", True,\
                            (255, 255, 255))
                    text_position = (100, 100)
                    self.surface.fill((0, 0, 0))
                    self.surface.blit(end_text_surface, text_position)
            else:
                self.surface.fill((200, 200, 200))
                square = (self.window - 2 * self.border) // cells_side
                mini_left = self.border + square * cells_side + self.border // 4
                mini_top = self.window // 2
                for turn in self.status.values():
                    if turn:
                        text_1 = f"Player {self.game.turn}"
                rect_width = 60
                rect_height = 200
                text_rect = pygame.Rect(mini_left, mini_top + 100,\
                    rect_width, rect_height)
                text_surface = font_player.render(text_1, True, (255, 255, 255))
                text_rect.center = text_rect.center
                text_rect.top -= 50
                text_position_rect = text_rect.copy()
                text_position_rect.x += 5
                text_position_rect.y += 5
                for i in range(1, self.game.num_players + 1):
                    counter_turn_text= f"P{i}: {self.game.player_counter[i]}"
                    counter_text_surface = font_player.render(counter_turn_text\
                        , True, color_dict[i][0])
                    counter_turn_rect = pygame.Rect(575, 75 + i*20, 30, 30)
                    self.surface.blit(counter_text_surface, counter_turn_rect)
                pygame.draw.rect(self.surface, color=(50, 90, 72),\
                    rect=text_rect)
                pygame.draw.rect(self.surface, (255, 255, 255), text_rect, 2)
                self.surface.blit(text_surface, text_position_rect)
                pygame.draw.circle(self.surface, color_dict[self.game.turn][0],
                    text_rect.center, self.window // 24 )
                for i in range(cells_side + 1):
                    pygame.draw.line(self.surface, (0, 0, 0), ((i + 1)* square\
                        - square + self.border, self.border), ((i + 1) * square\
                            - square + self.border, square * cells_side +\
                                self.border), 1)
                    pygame.draw.line(self.surface, (0, 0, 0), (self.border, i *\
                        square + self.border), (square * cells_side +\
                            self.border, i * square + self.border), 1)
                ###Checks for highlighted square (mouse hover)
                if self.highlight_square:
                    high_rect_x, high_rect_y = self.highlight_square
                    high_rect = self.recs_in_grid[high_rect_x][high_rect_y]
                    pygame.draw.rect(self.surface, color_dict[self.game.turn][\
                        0], high_rect, 20)
                ###Adds new "legal" ReversiRects to GUI Board
                moves = self.game.available_moves
                for i, row in enumerate(self.recs_in_grid):
                    for j, rect in enumerate(row):
                        if (i, j) in moves:
                            if rect is not None:
                                if not rect.legal:
                                    rect.legal = True
                            else:
                                legal_rect = ReversiRect(j * square +\
                                self.border, i * square + self.border, square,\
                                    square, True)
                                self.recs_in_grid[i][j] = legal_rect
                        else:
                            if rect is not None:
                                rect.make_illegal()
                for ind, row in enumerate(self.recs_in_grid):
                    for col, rect in enumerate(row):
                        if rect is not None:
                            if rect.legal and not rect.highlight:
                                pygame.draw.circle(self.surface,\
                                    color_dict[self.game.turn][1], ((col + 1)\
                        * square - square//2 + self.border, (ind + 1) * square\
                            - square// 2 + self.border), square // 2 -\
                                square // 10)
                                pygame.draw.circle(self.surface, GHOST_BLACK,\
                                    ((col + 1) * square - square//2 +\
                                        self.border, (ind + 1) * square -\
                                        square// 2 + self.border), square // 2\
                                            - square // 10, 2)
                for i in range(cells_side):
                    for j in range(cells_side):
                        if self.game.grid[i][j] is not None:
                            select_piece = self.game.grid[i][j]
                            pygame.draw.circle(self.surface,\
                                color_dict[select_piece][0], ((j + 1)\
                                    * square - square//2 + self.border, \
                                        (i + 1) * square - square// 2 +\
                                            self.border), square // 2 - square \
                                                // 10)
                            if select_piece == 1:
                                aux_color = WHITE
                            else:
                                aux_color = BLACK
                            pygame.draw.circle(self.surface, aux_color, \
                                ((j + 1) * square - square//2 + self.border,\
                                    (i + 1) * square - square// 2 + \
                                        self.border), square // 2 - square //\
                                            10, 2)
        self.surface.blit(self.game_surface, (self.border, self.border))

    def get_rect(self, loc: Tuple[int, int]):
        """
        Given a tuple that represents the mouse's position
        on the coordinate grid of the game window, the corresponding
        index (a, b) on the rectangle grid of ReversiGui is calculated.
        
        Returns:
            Tuple[Optional[Rect], Optional[Tuple[int, int]]]
        """
        cells_side = len(self.game.grid)
        square = (self.window - 2 * self.border) // cells_side
        x, y = loc
        a = (y - self.border) // square
        b = (x - self.border) // square
        if 0 <= a < cells_side and 0 <= b < cells_side:
            return (self.recs_in_grid[a][b], (a, b))
        return (None, None)

    def event_loop(self) -> None:
        """
        Handles user interactions

        Parameters: none beyond self

        Returns: nothing
        """
        while True:
            # Process Pygame events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if not self.start:
                    if event.type == pygame.MOUSEBUTTONUP:
                        mouse_pos_start = event.pos
                        if self.rect_button.collidepoint(mouse_pos_start):
                            self.start = True
                    if event.type == pygame.MOUSEMOTION:
                        if self.rect_button.collidepoint(event.pos):
                            self.start_button_status = True
                        else:
                            self.start_button_status = False
                else:
                    if event.type == pygame.MOUSEMOTION:
                        self.mouse_move = True
                        high_mouse_pos = event.pos
                        if self.get_rect(high_mouse_pos)[0] is not None:
                            if self.get_rect(high_mouse_pos)[0].legal:
                                self.highlight_square =\
                                    self.get_rect(high_mouse_pos)[1]
                            else:
                                self.highlight_square = None
                        else:
                            self.highlight_square = None
                    if event.type == pygame.MOUSEBUTTONUP:
                        mouse_pos = event.pos
                        if self.get_rect(mouse_pos)[0] is not None:
                            if self.get_rect(mouse_pos)[0] and\
                                self.get_rect(mouse_pos)[0].legal:
                                self.highlight_square = None
                                self.game.apply_move(self.get_rect(mouse_pos)[1]
                                                     )
            if self.game.done:
                self.draw_window()
                pygame.display.update()
                self.clock.tick(40)
                while self.game.done:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
            time_since_last_input = pygame.time.get_ticks() -\
                self.last_input_time
            if time_since_last_input < self.render_delay_threshold:
                pygame.display.flip()
            self.mouse_move = False
            self.draw_window()
            pygame.display.update()
            self.clock.tick(60)


class ReversiRect(pygame.Rect):
    """
    Subclass that inherits all attributes and methods of pygame.Rect objects
    but also has a "legal" and "highlight" attribute to support
    GUI design and Reversi game rules.
    """
    def __init__(self, x, y, width, height, legal: bool) -> None:
        super().__init__(x, y, width, height)
        self.highlight = False
        self.legal = legal

    def add_highlight(self, highlight):
        """
        Adds or removes highlight from ReversiRect object
        
        True adds, False removes.
        """
        self.highlight = highlight

    def make_illegal(self):
        """
        Makes a ReversiRect object illegal to remove from Gui
        
        Returns nothing
        """
        self.legal = False


@click.command()
@click.option('-n', '--num-players', type = click.INT, default = 2)
@click.option('-s', '--board-size', type = click.INT, default = 8)
@click.option('--othello', 'mode', flag_value = 'othello', default = True)
@click.option('--non-othello', 'mode', flag_value = 'non-othello')

def cmd(num_players: int, board_size: int, mode: str) -> None:
    """
    Allows specifications for playing reveersi in the terminal

    Args:
        num_players: number of play6ers
        board_size: size of the board
        mode: othello or not othello

    Returns: None
    """
    if mode == 'othello':
        game = ReversiGui(board_size, 600, 40, num_players, True)
    elif mode == 'non-othello':
        game = ReversiGui(board_size, 600, 40, num_players, False)
    game.event_loop()
if __name__ == "__main__":
    cmd()
