"""
Reversi implementation.

Contains a base class (ReversiBase). You must implement
a Reversi class that inherits from this base class.
"""
from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Dict, Tuple, Optional

PieceColor = Enum("PieceColor", ["BLACK", "WHITE", "RED", "GREEN", "YELLOW",
                                 "BLUE", "MAGENTA", "CYAN", "VIOLET"])
"""
Enum type for representing piece colors.
"""

color_dict = {1 : PieceColor["BLACK"], 2 : PieceColor["WHITE"], 3 : \
    PieceColor["RED"], 4 : PieceColor["GREEN"], 5: PieceColor["YELLOW"], 6: \
    PieceColor["BLUE"], 7: PieceColor["MAGENTA"], 8: PieceColor["CYAN"], \
    9: PieceColor["VIOLET"]}

class Piece:
    """
    A class to represent pieces of a game
    """

    def __init__(self, player: int, color: PieceColor, position: Tuple[int, \
        int]) -> None:
        """
        Constructor

        Args:
            player (int): what player the piece corresponds to
            color (PieceColor): the color of the piece
            position (Tuple[int, int]): the location of the piece
        """
        self.player = player
        self.color = color
        self.position = position
        self.dirx = [0, 0]

BoardGridType = List[List[Optional[int]]]
"""
Type for representing the state of the game board (the "grid")
as a list of lists. Each entry will either be an integer (meaning
there is a piece at that location for that player) or None,
meaning there is no piece in that location. Players are
numbered from 1.
"""

ListMovesType = List[Tuple[int, int]]
"""
Type for representing lists of moves on the board.
"""


class ReversiBase(ABC):
    """
    Abstract base class for the game of Reversi
    """

    _side: int
    _players: int
    _othello: bool

    def __init__(self, side: int, players: int, othello: bool):
        """
        Constructor

        Args:
            side: Number of squares on each side of the board
            players: Number of players
            othello: Whether to initialize the board with an Othello
            configuration.

        Raises:
            ValueError: If the parity of side and players is incorrect
        """
        self._side = side
        self._players = players
        self._othello = othello

    #
    # PROPERTIES
    #

    @property
    def size(self) -> int:
        """
        Returns the size of the board (the number of squares per side)
        """
        return self._side

    @property
    def num_players(self) -> int:
        """
        Returns the number of players
        """
        return self._players

    @property
    @abstractmethod
    def grid(self) -> BoardGridType:
        """
        Returns the state of the game board as a list of lists.
        Each entry can either be an integer (meaning there is a
        piece at that location for that player) or None,
        meaning there is no piece in that location. Players are
        numbered from 1.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def turn(self) -> int:
        """
        Returns the player number for the player who must make
        the next move (i.e., "whose turn is it?")  Players are
        numbered from 1.

        If the game is over, this property will not return
        any meaningful value.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def available_moves(self) -> ListMovesType:
        """
        Returns the list of positions where the current player
        (as returned by the turn method) could place a piece.

        If the game is over, this property will not return
        any meaningful value.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def done(self) -> bool:
        """
        Returns True if the game is over, False otherwise.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def outcome(self) -> List[int]:
        """
        Returns the list of winners for the game. If the game
        is not yet done, will return an empty list.
        If the game is done, will return a list of player numbers
        (players are numbered from 1). If there is a single winner,
        the list will contain a single integer. If there is a tie,
        the list will contain more than one integer (representing
        the players who tied)
        """
        raise NotImplementedError

    #
    # METHODS
    #

    @abstractmethod
    def piece_at(self, pos: Tuple[int, int]) -> Optional[int]:
        """
        Returns the piece at a given location

        Args:
            pos: Position on the board

        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.

        Returns: If there is a piece at the specified location,
        return the number of the player (players are numbered
        from 1). Otherwise, return None.
        """
        raise NotImplementedError

    @abstractmethod
    def legal_move(self, pos: Tuple[int, int]) -> bool:
        """
        Checks if a move is legal.

        Args:
            pos: Position on the board

        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.

        Returns: If the current player (as returned by the turn
        method) could place a piece in the specified position,
        return True. Otherwise, return False.
        """
        raise NotImplementedError

    @abstractmethod
    def apply_move(self, pos: Tuple[int, int]) -> None:
        """
        Place a piece of the current player (as returned
        by the turn method) on the board.

        The provided position is assumed to be a legal
        move (as returned by available_moves, or checked
        by legal_move). The behaviour of this method
        when the position is on the board, but is not
        a legal move, is undefined.

        After applying the move, the turn is updated to the
        next player who can make a move. For example, in a 4
        player game, suppose it is player 1's turn, they
        apply a move, and players 2 and 3 have no possible
        moves, but player 4 does. After player 1's move,
        the turn would be set to 4 (not to 2).

        If, after applying the move, none of the players
        can make a move, the game is over, and the value
        of the turn becomes moot. It cannot be assumed to
        take any meaningful value.

        Args:
            pos: Position on the board

        Raises:
            ValueError: If the specified position is outside
            the bounds of the board.

        Returns: None
        """
        raise NotImplementedError

    @abstractmethod
    def load_game(self, turn: int, grid: BoardGridType) -> None:
        """
        Loads the state of a game, replacing the current
        state of the game.

        Args:
            turn: The player number of the player that
            would make the next move ("whose turn is it?")
            Players are numbered from 1.
            grid: The state of the board as a list of lists
            (same as returned by the grid property)

        Raises:
             ValueError:
             - If the value of turn is inconsistent
               with the _players attribute.
             - If the size of the grid is inconsistent
               with the _side attribute.
             - If any value in the grid is inconsistent
               with the _players attribute.

        Returns: None
        """
        raise NotImplementedError

    @abstractmethod
    def simulate_moves(self,
                       moves: ListMovesType
                       ) -> "ReversiBase":
        """
        Simulates the effect of making a sequence of moves,
        **without** altering the state of the game (instead,
        returns a new object with the result of applying
        the provided moves).

        The provided positions are assumed to be legal
        moves. The behaviour of this method when a
        position is on the board, but is not a legal
        move, is undefined.

        Bear in mind that the number of *turns* involved
        might be larger than the number of moves provided,
        because a player might not be able to make a
        move (in which case, we skip over the player).
        Let's say we provide moves (2,3), (3,2), and (1,2)
        in a 3 player game, that it is player 2's turn,
        and that Player 3 won't be able to make any moves.
        The moves would be processed like this:

        - Player 2 makes move (2, 3)
        - Player 3 can't make any moves
        - Player 1 makes move (3, 2)
        - Player 2 makes move (1, 2)

        Args:
            moves: List of positions, representing moves.

        Raises:
            ValueError: If any of the specified positions
            is outside the bounds of the board.

        Returns: An object of the same type as the object
        the method was called on, reflecting the state
        of the game after applying the provided moves.
        """
        raise NotImplementedError

class Board():
    """
    Class to represent a game board.

    Attributes:
        size (int): size of side
        board (list): the game board
        piece_locations (dictionary): the location of each piece on the board

    Methods:
        add_piece: add a piece represented by a string to the board
    """
    _rows: int
    _cols: int
    _board: List[List[Optional[int]]]
    _piece_locations: Dict[int, List[Piece]]
    _ghost_locations: Dict[Tuple[int, int], List[Tuple[int, int]]]

    def __init__(self, size: int):
        self._rows = size
        self._cols = size
        self._board = [[None] * size for _ in range(size)]
        self._piece_locations = {}
        self._ghost_locations = {}

    @property
    def rows(self):
        """
        returns the number of rows
        """
        return self._rows

    @property
    def cols(self):
        """
        returns the number of columns
        """
        return self._cols

    @property
    def board(self):
        """
        returns the board
        """
        return self._board

    @property
    def piece_locations(self):
        """
        returns piece locations
        """
        return self._piece_locations

    @property
    def ghost_locations(self):
        """
        returns ghost piece locaations
        """
        return self._ghost_locations

    def add_piece(self, piece: Piece):
        """
        Add a piece represented by a Piece object to the board.

        Inputs:
            piece (Piece): the piece to add
        """
        loc = piece.position
        player = piece.player
        row, col = loc
        old_player = self.board[row][col]
        if old_player != player and old_player is not None:
            if old_player in self.piece_locations:
                for pc in self.piece_locations[old_player]:
                    if pc.position == loc:
                        self.piece_locations[old_player].remove(pc)
        self.board[row][col] = player
        if player in self.piece_locations:
            eq = Piece(player, color_dict[player], loc)
            self.piece_locations[player].append(eq)
        else:
            eq = Piece(player, color_dict[player], loc)
            self.piece_locations[player] = [eq]


    def add_ghost_piece(self, loc: Tuple[int, int], dirx : Tuple[int, int]):
        """
        Add a piece represented by a Piece object to the board.

        Inputs:
            piece (Piece): the piece to add
        """
        if loc in self.ghost_locations:
            if not dirx in self.ghost_locations[loc]:
                self.ghost_locations[loc].append(dirx)
        else:
            self.ghost_locations[loc] = [dirx]


    @property
    def is_full(self) -> bool:
        """
        Evaluates whether the board is full
        
        Returns (bool): True if there is a piece on every board square,
            False otherwise
        """
        for square in self.board:
            if None in square:
                return False
        return True

class Reversi(ReversiBase):
    """
    Class for the game of Reversi
    """

    def __init__(self, side: int, players: int, othello: bool):
        super().__init__(side, players, othello)
        if players > 9 or players < 2:
            raise ValueError("This implementation "
                             "only supports two - nine players")
        if side < 3:
            raise ValueError("The implementation must have a parity of \
                size 3 or above")
        if (side % 2 == self._players % 2) and side >= self._players:
            pass
        else:
            raise ValueError("Parity does not match")
        if othello and self._players != 2:
            raise ValueError("Othello variant only allowed for two players")
        self._grid = Board(side)
        self.center = self.produce_center_square()
        self.player_counter = {}
        if othello:
            self._grid.add_piece(Piece(2, PieceColor["WHITE"], \
                ((side // 2) - 1, (side // 2) - 1)))
            self._grid.add_piece(Piece(1, PieceColor["BLACK"], \
                ((side // 2) - 1, (side // 2))))
            self._grid.add_piece(Piece(2, PieceColor["WHITE"], ((side // 2), \
                (side // 2))))
            self._grid.add_piece(Piece(1, PieceColor["BLACK"], ((side // 2) , \
                (side // 2) - 1)))
            self._num_moves = 4
            for i in range(1, players + 1):
                self.player_counter[i] = 2
        else:
            self._num_moves = 0
            for i in range(1, players + 1):
                self._grid.piece_locations[i] = []
            for i in range(1, players + 1):
                self.player_counter[i] = 0
        self._turn = 1


    @property
    def size(self) -> int:
        return self._side

    @property
    def num_players(self) -> int:
        return self._players

    @property
    def grid(self) -> BoardGridType:
        return self._grid.board

    @property
    def turn(self) -> int:
        return self._turn

    @property
    def available_moves(self) -> ListMovesType:
        moves_lst = []
        for row in range(self._side):
            for col in range(self._side):
                if self.legal_move((row, col)):
                    moves_lst.append((row, col))
        return moves_lst

    @property
    def done(self) -> bool:
        turn = self._turn
        for _ in range(1, self._players + 1):
            if self.available_moves:
                self._turn = turn
                return False
            if self._turn == self.num_players:
                self._turn = 1
            else:
                self._turn += 1
        return True

    @property
    def outcome(self) -> List[int]:
        winner: List[int] = []
        if not self.done:
            return winner
        piece_dict = self._grid.piece_locations
        max_pieces = 0
        for pieces in piece_dict.values():
            if len(pieces) > max_pieces:
                max_pieces = len(pieces)
        for player, pieces in piece_dict.items():
            if len(pieces) == max_pieces:
                winner.append(player)
        return winner

    # Methods

    def piece_at(self, pos: Tuple[int, int]) -> Optional[int]:
        row, col = pos
        if not 0 <= row < self._side or not 0 <= col < self._side:
            raise ValueError("the specified position is outside the bounds of \
                the board")
        curr = self.grid[row][col]
        return curr

    def legal_move(self, pos: Tuple[int, int]) -> bool:
        row, column = pos
        if not 0 <= row < self._side or not 0 <= column < self._side:
            raise ValueError("the specified position is outside the bounds of \
                the board")
        if self.piece_at(pos):
            return False
        if self._num_moves < self.num_players ** 2 and not self._othello:
            self._grid.ghost_locations[pos] = []
            return pos in self.center

        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (-1, -1), (-1, 1),
                      (1, 1), (1, -1)]
        check = False
        for dirx in directions:
            move = self.can_move(pos, dirx)
            if move is not None:
                a, b = dirx
                a = -1 * a
                b = -1 * b
                self._grid.add_ghost_piece(pos, (a, b))
                check = True
        return check


    def produce_center_square(self) -> List[Tuple[int, int]]:
        """
        Gives the center squares that initial pieces need to be placed in
        
        Returns: a list of tuples that is all the squares in the center
        """
        result = []
        center = self._side // 2
        if self._side % 2 == 0:
            lower = center - (self.num_players // 2)
            upper = center + (self.num_players // 2) - 1
        else:
            lower = center - (self.num_players // 2)
            upper = center + (self.num_players // 2)
        for i in range(lower, upper + 1):
            for j in range(lower, upper + 1):
                result.append((i, j))
        return result

    def can_move(self, loc: Tuple[int, int],
                d: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """
        Determines if there is a move available for a piece in a certain
        direction in a game of Reversi

        Args:
            b (Board): the board
            loc (tuple[int, int]): location of interest
            d (tuple[int, int]): direction of interest

        Returns (tuple[int, int] or None): the available move or None if there 
            are no available moves
        """
        row, column = loc
        i, j = d
        curr = self.turn
        color = self._grid.board[row][column]
        if color is not None:
            return None
        max_rows = self._grid.rows - 1
        max_cols = self._grid.cols - 1
        row += i
        column += j
        if row > max_rows or row < 0 or column > max_cols or column < 0:
            return None
        check = self._grid.board[row][column]
        while isinstance(check, int) and check != curr:
            row += i
            column += j
            if row > max_rows or row < 0 or column > max_cols or column < 0:
                return None
            check = self._grid.board[row][column]
            if check == curr:
                return (row, column)
        return None


    def apply_move(self, pos: Tuple[int, int]) -> None:
        r, c = pos
        player = self.turn
        if not 0 <= r < self._side or not 0 <= c < self._side:
            raise ValueError("the specified position is outside the bounds of \
                the board")
        if not self.legal_move(pos):
            raise ValueError("move is not legal")

        dirx_list = self._grid.ghost_locations[pos]
        for dirx in dirx_list:
            to_update_list = []
            well_x, well_y = r, c
            dx, dy = dirx
            well_x -= dx
            well_y -= dy
            end = self._grid.board[well_x][well_y]
            correct = False
            while end is not None and end != player:
                to_update_list.append((well_x, well_y))
                well_x -= dx
                well_y -= dy
                if (well_x < 0 or well_x == self._side or
                    well_y < 0 or well_y == self._side):
                    break
                end = self._grid.board[well_x][well_y]
                if end == player:
                    correct = True
            if correct:
                for loc in to_update_list:
                    self.player_counter[self.piece_at(loc)] -= 1
                    self._grid.add_piece(Piece(player, color_dict[self._turn],
                                            (loc)))
                    self.player_counter[player] += 1

        self._grid.add_piece(Piece(self._turn, color_dict[self._turn], pos))
        self.player_counter[player] += 1
        curr = self._turn
        self._turn = self._turn % self.num_players + 1
        c = 0
        while curr != self._turn:
            if c != 0:
                self._turn = self._turn % self.num_players + 1
            c+= 1
            self._num_moves += 1
            if self.available_moves:
                break

    def load_game(self, turn: int, grid: BoardGridType) -> None:
        counter = 0
        if len(grid) != self._side or len(grid[0]) != self._side:
            raise ValueError("the size of the grid is inconsistent with the \
                _side attribute")
        if turn > self._players or turn < 0:
            raise ValueError("the value of turn is inconsistent with the \
                _players attribute")
        for row in grid:
            for col in row:
                if col is not None and (col > self._players or
                col < 0):
                    raise ValueError("value in the grid is inconsistent with \
                        the _players attribute")
        for i, row in enumerate(grid):
            for j, piece in enumerate(row):
                counter += 1
                if piece is not None:
                    to_add = Piece(piece, color_dict[piece], (i, j))
                    self._grid.add_piece(to_add)
                else:
                    self._grid.board[i][j] = None
        self._turn = turn
        self._num_moves = counter

    def simulate_moves(self, moves: ListMovesType) -> "ReversiBase":
        rev = Reversi(self._side, self._players, self._othello)
        rev.load_game(self.turn, self.grid)
        for move in moves:
            row, col = move
            if not 0 <= row < self._side or not 0 <= col < self._side:
                raise ValueError("the specified position is outside the bounds\
                    of the board")
            if rev.legal_move(move) and (move in rev.available_moves):
                rev.apply_move(move)
        return rev
