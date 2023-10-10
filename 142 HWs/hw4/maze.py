"""
CMSC 14200, Spring 2023
Homework #4

People Consulted:
   List anyone (other than the course staff) that you consulted about
   this assignment.

Online resources consulted:
   List the URLs of any online resources other than the course text and
   the official Python language documentation that you used to complete
   this assignment.
"""

from typing import List, Optional, Tuple, Set, Callable
from cell import Cell

# Characters for representing mazes as strings
WALL_CHARS = {
    "H_WALL": "─", "V_WALL": "│", "HV_WALL": "┼",
    "NW_CORNER": "┌", "NE_CORNER": "┐", "SW_CORNER": "└", "SE_CORNER": "┘",
    "VE_WALL": "├", "VW_WALL": "┤", "HS_WALL": "┬", "HN_WALL": "┴",
    "N_WALL": "╵", "E_WALL": "╶", "S_WALL": "╷", "W_WALL": "╴"
}

CURSOR = "•"
PATH = "·"

# Notice how box drawing character are always a combination
# of four possible lines starting at the center and going
# north, east, south, or west. For example:
#
#   north and east: "└"
#   east, west, and south: "┬"
#   west only: "╴"
#
# The following dictionary maps a tuple with four boolean
# values (corresponding to north, east, south, west) to
# the corresponding box drawing character. This dictionary
# should make it easier to select the appropriate character
# in various situations.
#
# (the name of the variable relates to the fact that we can
# also think of these directions as hands on a clock pointing
# to 12, 3, 6, or 9)
CLOCK_CHARS = {
    (False, False, False, False): " ",
    (False, False, False, True): WALL_CHARS["W_WALL"],
    (False, False, True, False): WALL_CHARS["S_WALL"],
    (False, False, True, True): WALL_CHARS["NE_CORNER"],
    (False, True, False, False): WALL_CHARS["E_WALL"],
    (False, True, False, True): WALL_CHARS["H_WALL"],
    (False, True, True, False): WALL_CHARS["NW_CORNER"],
    (False, True, True, True): WALL_CHARS["HS_WALL"],
    (True, False, False, False): WALL_CHARS["N_WALL"],
    (True, False, False, True): WALL_CHARS["SE_CORNER"],
    (True, False, True, False): WALL_CHARS["V_WALL"],
    (True, False, True, True): WALL_CHARS["VW_WALL"],
    (True, True, False, False): WALL_CHARS["SW_CORNER"],
    (True, True, False, True): WALL_CHARS["HN_WALL"],
    (True, True, True, False): WALL_CHARS["VE_WALL"],
    (True, True, True, True): WALL_CHARS["HV_WALL"]
}


class Maze:
    """
    A class for representing mazes
    """

    grid: List[List[Cell]]

    def __init__(self, filename: str):
        """
        Constructor

        Args:
            filename: File containing specification of a maze
        """
        with open(filename, encoding="utf-8") as f:
            lines = f.readlines()
        self.grid = []
        for line in lines:
            row = []
            for cell in line.split(","):
                row.append(Cell("N" in cell, "E" in cell))
            self.grid.append(row)

        # Make sure contents of grid are consistent
        assert all(len(row) == len(self.grid[0]) for row in self.grid), \
            f"Rows in {filename} don't all have the same length"
        assert not any(c.north for c in self.grid[0]), \
            f"Top row of {filename} includes cells with north set to True"
        assert not any(row[self.ncols-1].east for row in self.grid), \
            f"Rightmost column of {filename} includes " \
            f"cells with east set to True"

    @property
    def nrows(self) -> int:
        """
        Returns the number of rows in the maze
        """
        return len(self.grid)

    @property
    def ncols(self) -> int:
        """
        Returns the number of columns in the maze
        """
        return len(self.grid[0])

    def cell(self, at: Tuple[int, int]) -> Optional[Cell]:
        """
        Returns the cell (if any) at a given coordinate

        Args:
            at: Tuple with (row, col) coordinates

        Returns: Cell object at that location. If the location
            is outside the bounds of the maze, returns None.

        """
        row, col = at
        if not ((0 <= row < len(self.grid)) and (0 <= col < len(self.grid[0]))):
            return None

        return self.grid[row][col]

    def north(self, at: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """
        Returns the coordinates of the cell (if any) to the north of a cell.

        Args:
            at: Tuple with (row, col) coordinates

        Returns: If there exists a cell to the north of the cell
            at the given coordinates, *and* the two cells are
            connected, return the coordinates of the cell to the north.
            Otherwise, return None.
        """
        i, j = at
        if self.grid[i][j].north:
            return (i - 1, j)
        return None

    def east(self, at: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """
        Returns the coordinates of the cell (if any) to the east of a cell.

        Args:
            at: Tuple with (row, col) coordinates

        Returns: If there exists a cell to the east of the cell
            at the given coordinates, *and* the two cells are
            connected, return the coordinates of the cell to the east.
            Otherwise, return None.
        """
        i, j = at
        if self.grid[i][j].east:
            return (i, j + 1)
        return None

    def south(self, at: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """
        Returns the coordinates of the cell (if any) to the south of a cell.

        Args:
            at: Tuple with (row, col) coordinates

        Returns: If there exists a cell to the south of the cell
            at the given coordinates, *and* the two cells are
            connected, return the coordinates of the cell to the south.
            Otherwise, return None.
        """
        i, j = at
        if i + 1 >= len(self.grid):
            return None
        if self.grid[i + 1][j].north:
            return (i + 1, j)
        return None

    def west(self, at: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """
        Returns the coordinates of the cell (if any) to the west of a cell.

        Args:
            at: Tuple with (row, col) coordinates

        Returns: If there exists a cell to the west of the cell
            at the given coordinates, *and* the two cells are
            connected, return the coordinates of the cell to the west.
            Otherwise, return None.
        """
        i, j = at
        if j == 0:
            return None
        if self.grid[i][j - 1].east:
            return (i, j - 1)
        return None

    def to_string(self, path: Set[Tuple[int, int]],
                  at: Optional[Tuple[int, int]]) -> str:
        """
        Returns a string representation of the maze
        Args:
            path: Set of locations to highlight with
                the path character
            at: Location to highlight with the cursor
                character
        Returns: String representation
        """
        text_grid: List[List[str]] = []
        #making string representation grid 
        for i in range(0, (self.nrfows * 2 + 1)):
            str_list = []
            for j in range(0, (self.ncols * 2 + 1)):
                str_list.append(" ")
            text_grid.append(str_list)

        #setting up north and east walls for each cell
        for i, row in enumerate(self.grid):
            for j, cell in enumerate(row):
                if not cell.north:
                    text_grid[i * 2][j * 2 + 1] = CLOCK_CHARS[(False, True,
                        False, True)]
                if not cell.east:
                    text_grid[i * 2 + 1][j * 2 + 2] = CLOCK_CHARS[(True, False,
                        True, False)]

        #creating west and south walls of the entire string grid
        for i in range(3, len(text_grid) - 1, 2):
            text_grid[i][0] = CLOCK_CHARS[(True, False, True, False)]
        for j in range(1, len(text_grid[0]) - 2, 2):
            text_grid[len(text_grid) - 1][j] = CLOCK_CHARS[(False, True, False,
                True)]
    
        #creating shapes for the corners of each cell
        for i in range(0, len(text_grid), 2):
            for j in range(0, len(text_grid[0]), 2):
                text_grid[i][j] = CLOCK_CHARS[self.corner_bool((i, j), text_grid)]
        
        #special cases for the entry and exit cell corners (top left, bottom right)
        text_grid[0][0] = CLOCK_CHARS[(False, True, False, True)]
        text_grid[len(text_grid) - 1][len(text_grid[0]) - 1] = CLOCK_CHARS[(True,
            False, True, False)]

        #code for if the at and path parameter is not None/Empty
        if at is not None:
            i, j = at
            text_grid[i * 2 + 1][j * 2 + 1] = CURSOR
        for cord in path:
            i, j = cord
            text_grid[i * 2 + 1][j * 2 + 1] = PATH
        
        return "\n".join(["".join(row) for row in text_grid])

    def corner_bool(self, at: Tuple[int, int], 
        text_grid: List[List[str]]) -> Tuple[bool, bool, bool, bool]:
        """
        Looks at a given corner coordinate and returns a tuple of booleans
        representing the four cardinal directions.
        Inputs:
            at: Tuple with (row, col) coordinates
            text_grid: List of lists of strings representing a string 
                representation of our maze grid
        
        Returns: Tuple of booleans, with each boolean representing one of the 
            four cardinal directions and if there is a wall there. True if there
            is a wall, False otherwise.
        """
        directions = [(-1, 0), (0, 1), (1, 0), (0, -1)] #N, E, S, W
        ret = []
        i, j = at
        for dir in directions:
            if (i + dir[0] < 0 or j + dir[1] < 0 or i + dir[0] > len(text_grid) - 1
                or j + dir[1] > len(text_grid[0]) - 1):
                ret.append(False)
            elif text_grid[i + dir[0]][j + dir[1]] == " ":
                ret.append(False)
            else:
                ret.append(True)
        (N, E, S, W) = ret
        return (N, E, S, W)

    def __str__(self) -> str:
        """
        Returns a string representation with no path or cursor highlighted
        """
    
        return self.to_string(set(), None)

    def bfs(self) -> List[Tuple[int, int]]:
        """
        Does a BFS traversal starting at (0,0) and returns
        the shortest path to the bottom-right cell of the maze.

        Returns: List of coordinates of the cells that would be
            visited on the shortest path, starting at (0,0).
            The list must include (0,0) and the bottom-left coordinate.
        """
        source = (0, 0)
        shortest_path = [] 
        to_be_visited = []
        explored = set()
        previous_path = {} #dict mapping each coord to the coord that leads to it
        to_be_visited.append(source)
        while len(to_be_visited) > 0:
            current_cell = to_be_visited.pop(0) #dequeues first cell to be visited
            directions = [self.north(current_cell), self.east(current_cell), 
                          self.south(current_cell), self.west(current_cell)]
            explored.add(current_cell)
            for cell in directions:
                if cell not in explored and cell:
                    to_be_visited.append(cell)
                    explored.add(cell)
                    previous_path[cell] = current_cell
        position = (self.nrows - 1, self.ncols - 1) #this is the exit
        while position != source:
            shortest_path.append(position)
            position = previous_path[position] 
        shortest_path.append(source)
        shortest_path.reverse()
        return shortest_path

    def transform(
            self,
            transformer: Callable[["Maze", Tuple[int, int]], None]
            ) -> None:
        """
        Transforms the maze by applying a function to every cell of the maze.

        Args:
            transformer: Function that takes a Maze object and a tuple
                (representing the coordinates a cell) and transforms
                that cell is some way (does not return anything)

        Returns: Nothing
        """
        for idxr, row in enumerate(self.grid):
            for idxc, _ in enumerate(row):
                transformer(self, (idxr, idxc))

def open_all(maze: Maze, loc: Tuple[int, int]) -> None:
    """
    Takes a cell and connects it to the cells (if any)
    to the north, east, south, west (i.e., it "opens all the
    doors" of a cell)

    Args:
        maze: Maze object
        loc: Location (row, col) on the maze

    Returns: Nothing
    """
    i, j = loc
    cell = maze.grid[i][j]
    if not cell.north and i != 0:
        cell.north = True
    if not cell.east and j != (maze.ncols - 1):
        cell.east = True    

def open_dead_ends(maze: Maze, loc: Tuple[int, int]) -> None:
    """
    Takes a cell and, if it is a dead end (once in the cell,
    there you can only leave the cell by going back in the
    direction you came in), it creates a connection to
    the cell (if any) in the opposite direction to the existing
    connection.

    Args:
        maze: Maze object
        loc: Location (row, col) on the maze

    Returns: Nothing
    """
    i, j = loc
    row_in_bounds = 0 < i < (maze.nrows - 1)
    col_in_bounds = 0 < j < (maze.ncols - 1)
    try:
        if dead_end(maze, loc):
            if maze.north(loc) and row_in_bounds:
                maze.grid[i + 1][j].north = True
            elif maze.east(loc) and col_in_bounds:
                maze.grid[i][j - 1].east = True
            elif maze.south(loc) and row_in_bounds:
                maze.grid[i][j].north = True
            elif maze.west(loc) and col_in_bounds:
                maze.grid[i][j].east = True
    except IndexError:
        pass

def dead_end(maze: Maze, loc: Tuple[int, int]) -> bool:
    """
    Takes a cell checks if it is a dead end
    
    Args:
        maze: Maze object
        loc: Tuple[int, int]
        
    Returns [bool]: True if cell is dead end, false otherwise
    """
    surrounding_cells = [maze.north(loc), maze.west(loc),
                         maze.south(loc), maze.east(loc)]
    check = []
    if loc == (0,0):
        return False
    if loc == (maze.nrows - 1, maze.ncols - 1):
        return False
    for cell in surrounding_cells:
        check.append(cell)
    none_list = [x for x in check if x is not None]
    return len(none_list) == 1