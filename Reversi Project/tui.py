"""
TUI for Reversi
"""
from typing import Optional, List

import click
from colored import fore # type: ignore

from reversi import ReversiBase, Reversi, PieceColor

color_dict = {1 : PieceColor["BLACK"], 2 : PieceColor["WHITE"], 3 : \
    PieceColor["RED"], 4 : PieceColor["GREEN"], 5: PieceColor["YELLOW"], 6: \
    PieceColor["BLUE"], 7: PieceColor["MAGENTA"], 8: PieceColor["CYAN"], \
    9: PieceColor["VIOLET"]}

class TUIPlayer:
    """
    Simple class to store information about a TUI player

    A TUI player can either a human player using the keyboard,
    or a bot.
    """

    name: str
    reversi: Reversi
    color: PieceColor

    def __init__(self, n: int, reversi: Reversi, color: PieceColor):
        """
        Constructor

        Args:
            n: The player's number
            reversi: The Reversi game
            color: The player's color
        """
        self.name = f"Player {n}"
        self.reversi = reversi
        self.color = color

    def get_move(self) -> int:
        """
        Gets a move from the player

        Returns: None
        """
        while True:
            v = input(f"{self.name}> ")
            if v.isnumeric():
                col = int(v) - 1
                if -1 < col < len(self.reversi.available_moves):
                    return col
                else:
                    print("Invalid move, please select another")


def print_board(grid: List[List[Optional[int]]]) -> None:
    """
    Prints the board to the screen
    Args:
        grid: The board to print
    Returns: None
    """

    nrows = len(grid)
    ncols = len(grid[0])

    print(fore.WHITE + "┌" + ("─┬" * (ncols-1)) + "─┐")

    for r in range(nrows):
        crow = "│"
        for c in range(ncols):
            v = grid[r][c]
            if v is None:
                crow += " "
            elif v == 1:
                crow += fore.BLACK + "●"
            elif v == 2:
                crow += fore.WHITE + "●"
            elif v == 3:
                crow += fore.RED + "●"
            elif v == 4:
                crow += fore.GREEN + "●"
            elif v == 5:
                crow += fore.YELLOW + "●"
            elif v == 6:
                crow += fore.BLUE + "●"
            elif v == 7:
                crow += fore.MAGENTA + "●"
            elif v == 8:
                crow += fore.CYAN + "●"
            elif v == 9:
                crow += fore.VIOLET + "●"
            crow += fore.WHITE + "│"
        print(crow)

        if r < nrows - 1:
            print(fore.WHITE + "├" + ("─┼" * (ncols-1)) + "─┤")
        else:
            print(fore.WHITE + "└" + ("─┴" * (ncols-1)) + "─┘")

def play_reversi(reversi: ReversiBase,
                 players: list[TUIPlayer]) -> None:
    """
    Plays a game of reversi on the terminal
    
    Args:
        reversi: the Reversi game
        players: a list of TUIPlayers
        
    Returns: None
    """

    current = players[0]
    board = reversi.grid

    print()
    print_board(board)
    print()

    while not reversi.done:
        moves = reversi.available_moves
        print(f"It is {current.name}'s turn. Please choose a move:")
        for idx, val in enumerate(moves):
            i, j = val
            print(f"{idx + 1}: {j + 1, i + 1}")
        column = current.get_move()
        move = moves[column]
        reversi.apply_move(move)

        try:
            current = players[reversi.turn - 1]
        except IndexError:
            current = players[0]

        print()
        print_board(reversi.grid)

    winner = reversi.outcome
    if winner is not None and len(winner) == 1:
        num = winner[0]
        print(f"The winner is Player {num}!")
    else:
        print("It's a tie!")

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
        game = Reversi(board_size, num_players, True)
    elif mode == 'non-othello':
        game = Reversi(board_size, num_players, False)

    players = []
    for num in range(num_players):
        player_num = num + 1
        color = color_dict[player_num]
        player = TUIPlayer(player_num, game, color)
        players.append(player)
    play_reversi(game, players)

if __name__ == "__main__":
    cmd()
    