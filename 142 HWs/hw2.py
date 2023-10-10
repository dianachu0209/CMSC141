"""
CMSC 14200, Spring 2023
Homework #2

People Consulted:
   List anyone (other than the course staff) that you consulted about
   this assignment.

Online resources consulted:
   List the URLs of any online resources other than the course text and
   the official Python language documentation that you used to complete
   this assignment.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Union, Optional
from trees import ExprNode, BSTNode, BSTEmpty


#### Task 1 ####

class Boolean(ExprNode):
    """
    Class to represent a boolean value (True or False)
    """
    name: bool

    def __init__(self, name: bool):
        """
        Constructor

        Input:
            name (str): name of boolean being initialized
        """
        self.name = name

    def is_const(self) -> bool:
        """
        Evauates whether a node represents a constant value or is something 
        that needs to be evaluated further
        
        Returns (bool): True if value is a constant, False otherwise
        """
        return True
    
    def num_nodes(self) -> int:
        """
        Evaluates the number of nodes in the tree

        Returns (int): number of nodes in tree
        """
        return 1
    
    def eval(self) -> bool:
        """
        Evaluates the expression tree
        
        Returns (bool): True if value designates True, False otherwise
        """
        if self.name:
            return True
        else:
            return False
        
    def __str__(self) -> str:
        """
        Returns a string representation of the Boolean
        
        Returns (str): the string of the class
        """
        return str(self.name)

class BinaryOP(ExprNode):
    """
    Class to represent binary operators
    """
    val1: ExprNode
    val2: ExprNode

    def __init__(self, val1: ExprNode, val2: ExprNode):
        """
        Constructor

        Input:
            val1 (Boolean): boolean being initialized
            val2 (Boolean): second boolean being initialized
        """
        self.val1 = val1
        self.val2 = val2
    
    def is_const(self) -> bool:
        """
        Evauates whether a value is a constant
        
        Returns (bool): True if value is a constant, False otherwise
        """
        return False
    
    def num_nodes(self) -> int:
        """
        Evaluates the number of nodes in the tree

        Returns (int): number of nodes in tree
        """
        return 1 + self.val1.num_nodes() + self.val2.num_nodes()

class And(BinaryOP):
    """
    Class to represent the "and" operator
    """
    val1: ExprNode
    val2: ExprNode

    def __init__(self, val1: ExprNode, val2: ExprNode):
        """
        Constructor

        Input:
            val1 (Boolean): boolean being initialized
            val2 (Boolean): second boolean being initialized
        """
        super().__init__(val1, val2)
    
    def eval(self) -> bool:
        """
        Evaluates the expression tree
        
        Returns (bool): True if the expression evalutes to True, False otherwise
        """
        val1_val = self.val1.eval()
        val2_val = self.val2.eval()

        return val1_val and val2_val
        
    def __str__(self) -> str:
        """
        Returns a string representation of the Boolean
        
        Returns (str): the string of the class
        """
        val1_str = str(self.val1)
        val2_str = str(self.val2)

        return f"({val1_str} and {val2_str})"

class Or(BinaryOP):
    """
    Class to represent the "or" operator
    """
    val1: ExprNode
    val2: ExprNode

    def __init__(self, val1: ExprNode, val2: ExprNode):
        """
        Constructor

        Input:
            val1 (Boolean): boolean being initialized
            val2 (Boolean): second boolean being initialized
        """
        super().__init__(val1, val2)
    
    def eval(self) -> bool:
        """
        Evaluates the expression tree
        
        Returns (bool): True if the expression evalutes to True, False otherwise
        """
        val1_val = self.val1.eval()
        val2_val = self.val2.eval()

        return val1_val or val2_val
        
    def __str__(self) -> str:
        """
        Returns a string representation of the Boolean
        
        Returns (str): the string of the class
        """
        val1_str = str(self.val1)
        val2_str = str(self.val2)

        return f"({val1_str} or {val2_str})"

class Not(ExprNode):
    """
    Class to represent the "not" operator
    """
    val: ExprNode

    def __init__(self, val: ExprNode):
        """
        Constructor

        Input:
            val (Boolean): boolean being initialized
        """
        self.val = val
    
    def is_const(self) -> bool:
        """
        Evauates whether a value is a constant
        
        Returns (bool): True if value is a constant, False otherwise
        """
        return False
    
    def num_nodes(self) -> int:
        """
        Evaluates the number of nodes in the tree

        Returns (int): number of nodes in tree
        """
        return 1 + self.val.num_nodes()
    
    def eval(self) -> bool:
        """
        Negates the boolean
        
        Returns (bool): Negation of the input value
        """
        return not self.val.eval()
        
    def __str__(self) -> str:
        """
        Returns a string representation of the Boolean
        
        Returns (str): the string of the class
        """
        val_str = str(self.val)

        return f"(not {val_str})"

#### Task 2 ####

def verify_avl(t: Union[BSTEmpty, BSTNode]) -> bool:
    """
    Determine whether or not a BST is an AVL tree

    Input:
        t (BST): the tree

    Returns (bool): True if t is an AVL tree, False otherwise
    """
    if t.num_nodes < 3 or t.is_empty:
        return True
    else:
        assert isinstance(t, BSTNode)
        if t.balance_factor in range(-1, 2):
            left = verify_avl(t.left)
            right = verify_avl(t.right)
            if left and right:
                return True
        return False  


#### Task 3 ####

class BSTEmptyOpt:
    """
    Empty (Optimized) BST Tree
    """

    # No constructor needed (nothing to initialize)

    @property
    def is_empty(self) -> bool:
        """
        Returns: True if the tree is empty, False otherwise
        """
        return True

    @property
    def is_leaf(self) -> bool:
        """
        Returns: True if the tree is a leaf node, False otherwise
        """
        return False

    @property
    def num_nodes(self) -> int:
        """
        Returns: The number of nodes in the tree
        """
        return 0

    @property
    def height(self) -> int:
        """
        Returns: The height of the tree
        """
        return 0

    def contains(self, n: int) -> bool:  # pylint: disable=unused-argument
        """
        Determines whether a value is contained in the tree.

        Args:
            n: The value to check

        Returns: True if the value is contained in the tree,
            False otherwise.
        """
        return False

    def insert(self, n: int) -> "BSTNodeOpt":
        """
        Inserts a value into the tree

        Args:
            n: Value to insert

        Returns: A new tree with the value inserted into it
        """
        return BSTNodeOpt(n, BSTEmptyOpt(), BSTEmptyOpt())


class BSTNodeOpt:
    """
    (Optimized) BST Tree Node
    """

    value: int
    left: Union[BSTEmptyOpt, "BSTNodeOpt"]
    right: Union[BSTEmptyOpt, "BSTNodeOpt"]
    count: int

    def __init__(self, n: int,
                 left: Union[BSTEmptyOpt, "BSTNodeOpt"],
                 right: Union[BSTEmptyOpt, "BSTNodeOpt"]):
        """
        Constructor

        Args:
            n: Value associated with the tree node
            left: Left child tree
            right: Right child tree
        """
        self.value = n
        self.left = left
        self.right = right
        self.count = 1
        if self.left.is_empty and (not self.right.is_empty):
            self.count += 1
        elif (not self.left.is_empty) and self.right.is_empty:
            self.count += 1
        elif not (self.left.is_empty and self.right.is_empty):
            assert isinstance(self.left, BSTNodeOpt)
            assert isinstance(self.right, BSTNodeOpt)
            if self.left.is_leaf and self.right.is_leaf:
                self.count += 2
            else:
                self.count += self.left.count + self.right.count

    @property
    def is_empty(self) -> bool:
        """
        Returns: True if the tree is empty, False otherwise
        """
        return False

    @property
    def is_leaf(self) -> bool:
        """
        Returns: True if the tree is a leaf node, False otherwise
        """
        return self.left.is_empty and self.right.is_empty

    @property
    def num_nodes(self) -> int:
        """
        Returns: The number of nodes in the tree
        """
        return self.count

    @property
    def height(self) -> int:
        """
        Returns: The height of the tree
        """
        return 1 + max(self.left.height, self.right.height)

    @property
    def balance_factor(self) -> int:
        """
        Returns: Balance factor of the tree
        """
        return self.right.height - self.left.height

    def contains(self, n: int) -> bool:
        """
        Determines whether a value is contained in the tree.

        Args:
            n: The value to check

        Returns: True if the value is contained in the tree,
            False otherwise.
        """
        if n < self.value:
            return self.left.contains(n)
        elif n > self.value:
            return self.right.contains(n)
        else:
            return True

    def insert(self, n: int) -> "BSTNodeOpt":
        """
        Inserts a value into the tree

        Args:
            n: Value to insert

        Returns: A new tree with the value inserted into it
        """
        if n < self.value:
            return BSTNodeOpt(self.value, self.left.insert(n), self.right)
        elif n > self.value:
            return BSTNodeOpt(self.value, self.left, self.right.insert(n))
        else:
            return self


#### Task 4 ####

class Board:
    """
    Class to represent a game board.

    Attributes:
        rows (int): number of rows
        cols (int): number of columns
        board (list): the game board
        location_of_pieces (dictionary): the location of each piece on the board

    Methods:
        add_piece: add a piece represented by a string to the board
    """
    rows: int
    cols: int
    board: List[List[Optional[str]]]
    location_of_pieces: Dict[str, List[Tuple[int, int]]]

    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.board = [[None] * cols for _ in range(rows)]
        self.location_of_pieces = {}

    def add_piece(self, piece: str, location: Tuple[int, int]) -> bool:
        """
        Add a piece represented by a string to the board.

        Inputs:
            piece (string): the piece to add
            location (tuple): the (row, column) location of where to add
                the piece

        Returns (bool): True if the piece was added successfully,
            False otherwise
        """
        row, col = location

        if self.board[row][col] is None:
            self.board[row][col] = piece
            if piece in self.location_of_pieces:
                self.location_of_pieces[piece].append(location)
            else:
                self.location_of_pieces[piece] = [location]
            return True
        return False

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

#### Task 5 ####

def can_move(b: Board, loc: Tuple[int, int], 
             d: Tuple[int, int]) -> Optional[Tuple[int, int]]:
    """
    Determines if there is a move available for a piece in a certain
    direction in a two player game of Reversi

    Args:
        b (Board): the board
        loc (tuple[int, int]): location of interest
        d (tuple[int, int]): direction of interest

    Returns (tuple[int, int] or None): the available move or None if there are
        no available moves
    """
    row, column = loc
    i, j = d
    color = b.board[row][column]
    max_rows = b.rows - 1
    max_cols = b.cols - 1
    row += i
    column += j
    if row > max_rows or row < 0 or column > max_cols or column < 0:
        return None
    check = b.board[row][column]
    while check is not None and check != color:
        row += i
        column += j
        if row > max_rows or row < 0 or column > max_cols or column < 0:
            return None
        check = b.board[row][column]
        if check is None:
            return (row,column)
        if check == color:
            return None   
    return None

def get_moves(b: Board, piece: str) -> List[Tuple[int, int]]:
    """
    Get all possible moves for a piece in a two player game of Reversi

    Input:
        b (Board): the board
        piece (string): the piece

    Return (list of tuples): A list of all possible moves for
        piece on the Reversi board b, according to the rules of Reversi
    """
    possible_moves = []
    d = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]
    for location in b.location_of_pieces[piece]:
        for direction in d:
            if can_move(b, location, direction) is not None:
                if can_move(b, location, direction) in possible_moves:
                    continue
                move = can_move(b, location, direction)
                assert isinstance(move, tuple)
                possible_moves.append(move)
    return possible_moves