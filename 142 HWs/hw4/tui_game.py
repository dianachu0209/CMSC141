"""
CMSC 14200, Spring 2023
Homework #4
"""

import sys
from maze import Maze, open_all, open_dead_ends

maze = Maze(f"{sys.argv[1]}")
#checking if there is a specified difficulty
if len(sys.argv) > 2:
    difficulty = sys.argv[2]
else:
    difficulty = " "

if difficulty == "easy":
    maze.transform(open_dead_ends)
if difficulty == "super-easy":
    maze.transform(open_all)

cursor = (0, 0) #start/current position of player
end = (maze.nrows - 1, maze.ncols - 1)
directions = {"w": (-1, 0), "a": (0, -1), "s": (1, 0), "d": (0, 1)}
wall_message = "There is a wall in the way"
while cursor != end:
    print(maze.to_string(set(), cursor))
    direction = input()
    try:
        if direction == "w" and maze.north(cursor) is None:
            print(wall_message)
            continue
        elif direction == "s" and maze.south(cursor) is None:
            print(wall_message)
            continue
        elif direction == "d" and maze.east(cursor) is None:
            print(wall_message)
            continue
        elif direction == "a" and maze.west(cursor) is None:
            print(wall_message)
            continue
    except KeyError:
        print("Please enter w, a, s, or d")
    cursor = (cursor[0] + directions[direction][0], cursor[1] + 
        directions[direction][1])

if cursor == end:
    print(maze.to_string(set(), cursor))
    print("You made it out!")
