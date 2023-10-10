"""
CMSC 14200, Spring 2023
Homework #1

People Consulted:
   List anyone (other than the course staff) that you consulted about
   this assignment.

Online resources consulted:
   List the URLs of any online resources other than the course text and
   the official Python language documentation that you used to complete
   this assignment.
"""

from typing import List, Tuple, Dict, Union, Optional
from abc import ABC, abstractmethod
from math import pi

from tree import TreeNode


def words_that_start_with(list_of_words: list, char_to_match: str) -> int:
    """
    Count the number of words in a list whose first character matches
    the given character to match.

    Inputs:
        list_of_words (list): the list of words
        char_to_match (string): the character to match

    Returns (int): the number of words that start with char_to_match
    """
    count = 0
    for word in list_of_words:
        if word[0] == char_to_match:
            count += 1
    return count


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
    board: List[List[Union[int, str, None]]]
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

def num_repeated_ancestors_r(t: TreeNode, ancestor_value: int) -> int:
    """
    Recursively finds the number of nodes in a tree that have the
        same value as an ancestor.

    Inputs:
        t (TreeNode): the tree
        ancestor_value (int): the value of the ancestor being checked
    
    Returns (int): the number of nodes with the same value as one ancestor
    """
    count = 0
    if t.value == ancestor_value:
        count += 1
    for child in t.children:
        count += num_repeated_ancestors_r(child, ancestor_value)
        count += num_repeated_ancestors_r(child, t.value)
    return count


def num_repeated_ancestors(t: TreeNode) -> int:
    """
    Find the number of nodes in a tree that have the
        same value as one of their ancestors.

    Inputs:
        t (TreeNode): the tree

    Returns (int): the number of nodes
    """
    count = 0
    for child in t.children:
        count += num_repeated_ancestors_r(child, t.value)
    return count

class Shape(ABC):
    """
    Class to represent a shape.

    Methods:
        area: compute the area of the shape
        perimeter: compute the perimeter of the shape
        is_symmetric: determines whether or not the shape is symmetric
            with respect to 90 degree clockwise rotation
    """

    @abstractmethod
    def area(self) -> float:
        """
        Computes the area of the shape

        Returns (float): Area of the shape
        """
        raise NotImplementedError

    @abstractmethod
    def perimeter(self) -> float:
        """
        Computes the perimeter of the shape

        Returns (float): Perimeter of the shape
        """
        raise NotImplementedError

    @abstractmethod
    def is_symmetric(self) -> bool:
        """
        Checks whether the shape is symmetric

        Returns (bool): True if the shape is symmetric,
            False otherwise.
        """
        raise NotImplementedError


class Circle(Shape):
    """
    Class to represent a circle.
    """
    def __init__(self, radius: Union[float, int]):
        """
        Constructor

        Input:
            radius (float, int): radius
        """
        self.radius = radius

    def area(self) -> float:
        """
        Computes the area of the circle

        Returns (float): Area of the circle
        """
        return pi * self.radius**2

    def perimeter(self) -> float:
        """
        Computes the perimeter of the circle

        Returns (float): Perimeter of the circle
        """
        return 2 * pi * self.radius

    def is_symmetric(self) -> bool:
        """
        Checks whether the shape is symmetric

        Returns (bool): True if the shape is symmetric,
            False otherwise.
        """
        return True


class Rectangle(Shape):
    """
    Class to represent a rectangle.
    """
    def __init__(self, length: Union[float, int], width: Union[float, int]):
        """
        Constructor

        Input:
            radius (float, int): radius
        """
        self.length = length
        self.width = width

    def area(self) -> float:
        """
        Computes the area of the rectangle

        Returns (float): Area of the rectangle
        """
        return self.length * self.width

    def perimeter(self) -> float:
        """
        Computes the perimeter of the rectangle

        Returns (float): Perimeter of the rectangle
        """
        return (2 * self.length) + (2 * self.width)

    def is_symmetric(self) -> bool:
        """
        Checks whether the rectangle is symmetric

        Returns (bool): True if the rectangle is symmetric,
            False otherwise.
        """
        return self.length == self.width

class Square(Rectangle):
    """
    Class to represent a square.
    """
    def __init__(self, length: Union[float, int]):
        """
        Constructor

        Input:
            radius (float, int): radius
        """
        super().__init__(length, length)
