"""
CMSC 14200, Spring 2023
Homework #4
"""

import sys
from maze import Maze

maze = Maze(f"{sys.argv[1]}")
print(maze.to_string(set(maze.bfs()), None))
