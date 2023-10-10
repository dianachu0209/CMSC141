"""
Mock implementations of ReversiBase.

We provide a ReversiStub implementation, and you must
implement a ReversiMock implementation.
"""
from typing import List, Tuple, Optional
from copy import deepcopy

from reversi import ReversiBase, BoardGridType, ListMovesType


class ReversiStub(ReversiBase):
    """
    Stub implementation of ReversiBase.

    This stub implementation behaves according to the following rules:

    - It only supports two players and boards of size 2x2 and above.
    - The board is always initialized with four pieces in the four corners
      of the board. Player 1 has pieces in the northeast and southwest
      corners of the board, and Player 2 has pieces in the southeast and
      northwest corners of the board.
    - All moves are legal, even if there is already a piece in a given position.
    - The game ends after four moves. Whatever player has a piece in position
      (0,1) wins. If there is no piece in that position, the game ends in a tie.
    - It does not validate board positions. If a method
      is called with a position outside the board, the method will likely cause
      an exception.
    - It does not implement the ``load_game`` or ``simulate_moves`` method.
    """

    _grid: BoardGridType
    _turn: int
    _num_moves: int

    def __init__(self, side: int, players: int, othello: bool):
        if players != 2:
            raise ValueError("The stub implementation "
                             "only supports two players")

        super().__init__(side, players, othello)

        self._grid = [[None]*side for _ in range(side)]
        self._grid[0][-1] = 1
        self._grid[-1][0] = 1
        self._grid[0][0] = 2
        self._grid[-1][-1] = 2

        self._turn = 1
        self._num_moves = 0

    @property
    def grid(self) -> BoardGridType:
        return deepcopy(self._grid)

    @property
    def turn(self) -> int:
        return self._turn

    @property
    def available_moves(self) -> ListMovesType:
        moves = []
        for r in range(self._side):
            for c in range(self._side):
                moves.append((r, c))

        return moves

    @property
    def done(self) -> bool:
        return self._num_moves == 4

    @property
    def outcome(self) -> List[int]:
        if not self.done:
            return []

        if self._grid[0][1] is None:
            return [0, 1]
        else:
            return [self._grid[0][1]]

    def piece_at(self, pos: Tuple[int, int]) -> Optional[int]:
        r, c = pos
        return self._grid[r][c]

    def legal_move(self, pos: Tuple[int, int]) -> bool:
        return True

    def apply_move(self, pos: Tuple[int, int]) -> None:
        r, c = pos
        self._grid[r][c] = self._turn
        self._turn = 2 if self._turn == 1 else 1
        self._num_moves += 1

    def load_game(self, turn: int, grid: BoardGridType) -> None:
        raise NotImplementedError()

    def simulate_moves(self,
                       moves: ListMovesType
                       ) -> ReversiBase:
        raise NotImplementedError()

class ReversiMock(ReversiBase):
    """
    Mock implementation of ReversiBase.
    
    x supports two players and boards of size 4x4 and above.
    x validates the parity of the board size (since we only support two players,
      it just needs to validate that the side of the board has an even size)
    x supports the othello parameter to the constructor to initialize the 
      board's center square. Since we only support two players, we can just 
      manually set the center four squares to the expected values.
    X raise ValueError exceptions as specified in the ReversiBase docstrings.
    X a move is legal if the position in the board is empty, and there is at 
      least one piece (of any player) in an adjacent square (in any direction, 
      including diagonals). Additionally, placing a piece in position (0,0) or 
      (side-1, side-1) is always legal.
    X if a player places a piece in position (0,0), the game ends, 
      and that player wins the game.
    X if a player places a piece in position (side-1, side-1), the game ends, 
      and both players win the game (i.e., the game ends in a tie)
    X does not implement the load_game method.
    - only needs to support simulating a single move in simulate_moves.
    """

    _grid: BoardGridType
    _turn: int
    _num_moves: int

    def __init__(self, side: int, players: int, othello: bool):
        if players != 2:
            raise ValueError("The mock implementation "
                             "only supports two players")
        if side < 4:
            raise ValueError("The mock implementation must have a parity of \
                size 4 or above")
        if side % 2 == 0:
            pass
        else:
            raise ValueError("temp way to verify parity")

        super().__init__(side, players, othello)
        self._grid = [[None]*side for _ in range(side)]
        if othello:
            self._grid[(side // 2) - 1][(side // 2) - 1] = 2
            self._grid[side // 2][side // 2] = 2
            self._grid[(side // 2) - 1][(side // 2)] = 1
            self._grid[(side // 2)][(side // 2) - 1] = 1

        self._turn = 1
        self._num_moves = 0

    @property
    def grid(self) -> BoardGridType:
        return deepcopy(self._grid)

    @property
    def turn(self) -> int:
        return self._turn

    @property
    def available_moves(self) -> ListMovesType:
        moves = []
        for row in range(self._side):
            for col in range(self._side):
                if self.legal_move((row, col)):
                    moves.append((row, col))
        return moves


    @property
    def done(self) -> bool:
        top_fill = self._grid[0][0] is not None
        bottom_fill = self._grid[self._side - 1][self._side - 1] is not None
        return top_fill or bottom_fill

    @property
    def outcome(self) -> List[int]:
        if not self.done:
            return []
        if self._grid[self._side - 1][self._side - 1] is not None:
            return [1, 2]
        return [self._grid[0][0]]

    def piece_at(self, pos: Tuple[int, int]) -> Optional[int]:
        r, c = pos
        if not 0 <= r < self._side or not 0 <= c < self._side:
            raise ValueError("the specified position is outside the bounds of \
                the board")

        return self._grid[r][c]

    def legal_move(self, pos: Tuple[int, int]) -> bool:
        r, c = pos
        if (r == 0 and c == 0) or (r == self._side - 1 and c == self._side - 1):
            return True
        if not 0 <= r < self._side or not 0 <= c < self._side:
            raise ValueError("the specified position is outside the bounds of \
                the board")
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (-1, -1), (-1, 1),
                      (1, 1), (1, -1)]
        if not self._grid[r][c]:
            for dir in directions:
                dx, dy = dir
                pos_y = r + dy
                pos_x = c + dx
                if pos_y > (self._side - 1) or pos_y < 0 or pos_x >\
                    (self._side - 1) or pos_x < 0:
                    continue
                if self._grid[pos_y][pos_x]:
                    return True
        return False

    def apply_move(self, pos: Tuple[int, int]) -> None:
        r, c = pos
        if not 0 <= r < self._side or not 0 <= c < self._side:
            raise ValueError("the specified position is outside the bounds of \
                the board")
        self._grid[r][c] = self._turn
        self._turn = 2 if self._turn == 1 else 1
        self._num_moves += 1

    def load_game(self, turn: int, grid: BoardGridType) -> None:
        if turn > self._players or turn < 0:
            raise ValueError("the value of turn is inconsistent with the \
                _players attribute")
        if len(grid) != self._side or len(grid[0]) != self._side:
            raise ValueError("the size of the grid is inconsistent with the \
                _side attribute")
        for r in grid:
            for c in r:
                if c is not None or int(c) > self._players or int(c) < 0:
                    raise ValueError("value in the grid is inconsistent with \
                        the _players attribute")
        raise NotImplementedError()

    def simulate_moves(self,
                       moves: ListMovesType
                       ) -> ReversiBase:
        result_reversi = ReversiMock(self._side, self._players, self._othello)
        for move in moves:
            r, c = move
            if not 0 <= r < self._side or not 0 <= c < self._side:
                raise ValueError("the specified position is outside the bounds\
                    of the board")
            if self.legal_move(move) and (move in self.available_moves):
                result_reversi.apply_move(move)
        return result_reversi

class ReversiBotMock(ReversiMock):

    @property
    def done(self):

        for row in self._grid:
            for val in row:
                if val is None:
                    return False
        return True

    @property
    def outcome(self):
        player_1_piece_count: int = 0
        player_2_piece_count: int = 0

        if not self.done:
            return []

        for row in self._grid:
            for val in row:
                if val == 1:
                    player_1_piece_count += 1
                if val == 2:
                    player_2_piece_count +=1
        if player_1_piece_count > player_2_piece_count:
            return [1]
        elif player_1_piece_count < player_2_piece_count:
            return [2]
        else:
            return [1,2]

    def legal_move(self, pos: Tuple[int, int]) -> bool:
        r, c = pos
        if not 0 <= r < self._side or not 0 <= c < self._side:
            raise ValueError("the specified position is outside the bounds of \
                the board")
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (-1, -1), (-1, 1),
                      (1, 1), (1, -1)]
        if not self._grid[r][c]:
            for dirx in directions:
                dx, dy = dirx
                pos_y = r + dy
                pos_x = c + dx
                if pos_y > (self._side - 1) or pos_y < 0 or pos_x >\
                    (self._side - 1) or pos_x < 0:
                    continue
                if self._grid[pos_y][pos_x]:
                    return True
        return False

    def apply_move(self, pos: Tuple[int, int]) -> None:
        opp_turn: int
        if self._turn == 1:
            opp_turn = 2
        else: 
            opp_turn = 1
        r, c = pos
        if not 0 <= r < self._side or not 0 <= c < self._side:
            raise ValueError("the specified position is outside the bounds of \
                the board")
        self._grid[r][c] = self._turn
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0), 
                      (-1, -1), (-1, 1),(1, 1), (1, -1)]
        for direction in directions:
            dx,dy = direction
            pos_y = r + dy
            pos_x = c + dx 
            if pos_y > (self._side - 1) or pos_y < 0 or (pos_x >
            (self._side - 1) or pos_x < 0):
                continue
            if self._grid[pos_y][pos_x] == opp_turn:
                self._grid[pos_y][pos_x] = self._turn
        self._turn = 2 if self._turn == 1 else 1
        self._num_moves += 1

    def simulate_moves(self, moves: ListMovesType) -> ReversiMock:
        result = ReversiBotMock(self._side, self._players, self._othello)
        for move in moves:
            r, c = move
            if not 0 <= r < self._side or not 0 <= c < self._side:
                raise ValueError("the specified position is outside the bounds\
                    of the board")
            if self.legal_move(move) and (move in self.available_moves):
                ### once available_moves works it should work
                super().apply_move(move)
        return result
            