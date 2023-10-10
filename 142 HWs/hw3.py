"""
CMSC 14200, Spring 2023
Homework #3

People Consulted:
   List anyone (other than the course staff) that you consulted about
   this assignment.

Online resources consulted:
   List the URLs of any online resources other than the course text and
   the official Python language documentation that you used to complete
   this assignment.
"""
from typing import List, Set, Dict, Tuple

from graph import Vertex, Graph


#### Task 1 ####

def num_indegree_gt_outdegree(graph: Graph) -> int:
    """
    Count how many vertices have in-degree > out-degree

    Input:
        graph (Graph): the graph

    Returns (int): the count
    """
    indegree_dict: Dict[str, int] = {}
    outdegree_dict = {}
    count = 0
    for vertex_name, vertex in graph.vertices.items():
        for dest in vertex.edges_to:
            indegree_dict[dest] = indegree_dict.get(dest, 0) + 1
        outdegree_dict[vertex_name] = len(vertex.edges_to.keys())
    for name, indegree in indegree_dict.items():
        if outdegree_dict.get(name, 0) < indegree:
            count += 1
    return count   

#### Task 2 ####

def reachable_in(graph: Graph, vertex: str, hops: int) -> Set[str]:
    """
    Determine the set of vertices in a graph reachable from a starting point in
    at most "hops" steps

    Inputs:
        graph (Graph): the graph
        vertex (str): the name of the starting vertex
        hops (int): the maximum number of steps away from the starting point

    Returns (Set[str]): the names of vertices reachable under the constraint
    """
    source = graph.get_vertex(vertex)
    assert isinstance(source, Vertex)
    reachable = set()
    to_be_visited = []
    to_be_visited.append((source, 0))
    while len(to_be_visited) > 0:
        current_node, dist = to_be_visited.pop(0)
        if dist > hops:
            continue
        reachable.add(current_node.name)
        for _, child in current_node.edges_to.items():
            if child.name in reachable:
                continue
            to_be_visited.append((child, dist + 1))
    return reachable

#### Task 3 ####

def flood_fill(grid: List[List[bool]], start: Tuple[int, int]) -> None:
    """
    "Flood fill" (the paint-bucket tool) a grid of booleans
    Change a cell in the grid to black (True) and its neighboring cell, and
    their neighbors, stopping when encountering an already-black (True) cell in
    a given direction
    Directions are N, E, S, and W, but not diagonal

    Inputs:
        grid (List[List[bool]]): two-dimensional grid of boolean cells
        start (Tuple[int, int]): the coordinates of the starting cell
            Returns: nothing
        """
    row, column = start
    surrounding = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    if grid[row][column]:
        return
    grid[row][column] = True
    for i, j in surrounding:
        n_row, n_column = row + i, column + j
        if 0 <= n_row < len(grid) and 0 <= n_column < len(grid[0]):
            if not grid[n_row][n_column]:
                flood_fill(grid, (n_row, n_column))
