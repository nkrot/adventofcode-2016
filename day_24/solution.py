#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List, Tuple, Optional, Union
import copy

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils

DAY = '24'
DEBUG = False


class POI(object):
    '''Point of interest'''

    def __init__(self, xy: Tuple[int, int], value: str = None):
        self.xy = tuple(xy)
        self.value = str(value)
        self.distance = 0

    @property
    def x(self):
        return self.xy[0]

    @property
    def y(self):
        return self.xy[1]

    def __add__(self, other: Tuple[int, int]):
        xy = (self.xy[0] + other[0], self.xy[1] + other[1])
        return type(self)(xy)

    def __repr__(self):
        return "<{}: xy={}, value={}, distance={}>".format(
            self.__class__.__name__, self.xy, self.value, self.distance)


class Maze(object):

    @classmethod
    def from_lines(cls, lines: List[str]):
        obj = cls()
        for ri, row in enumerate(lines):
            chars = list(row)
            obj.rows.append(chars)
            for ci, char in enumerate(chars):
                if char.isdigit():
                    obj.points.append(POI((ri, ci), char))
        return obj

    def __init__(self):
        self.rows = []
        self.points = []

    def __copy__(self):
        obj = type(self)()
        obj.rows = [list(r) for r in self.rows]
        obj.points = list(self.points)
        return obj

    def __getitem__(self, xy: Union[POI, Tuple]) -> Optional[str]:
        if isinstance(xy, POI):
            xy = xy.xy
        r, c = xy
        if 0 <= r < len(self.rows) and 0 <= c < len(self.rows[r]):
            return self.rows[r][c]
        return None

    def __setitem__(self, xy: Union[POI, Tuple], val):
        if isinstance(xy, POI):
            xy = xy.xy
        r, c = xy
        if 0 <= r < len(self.rows) and 0 <= c < len(self.rows[r]):
            self.rows[r][c] = val

    def __str__(self):
        lines = ["".join(r) for r in self.rows]
        return "\n".join(lines)

    def point(self, value: str) -> Optional[POI]:
        '''Find the point having value <value>.
        >>> maze.point(0)
        >>> maze.point(3)
        '''
        val = str(value)
        for pt in self.points:
            if pt.value == val:
                return pt


class Edge(object):

    def __init__(self, p1: POI, p2: POI, weight: int = 0):
        self.points = [p1, p2]
        self.weight = weight

    @property
    def start(self):
        return self.points[0]

    @property
    def end(self):
        return self.points[1]

    def __eq__(self, other: 'Edge') -> bool:
        return (self.start.xy == other.start.xy
                and self.end.xy == other.end.xy
                and self.weight == other.weight)

    def __repr__(self):
        return "<{}: points={}, weight={}>".format(
            self.__class__.__name__, self.points, self.weight)


class Graph(object):
    '''A collection of edges'''

    def __init__(self):
        self.edges = []

    def extend(self, edges: List[Edge]):
        self.edges.extend(list(edges))

    def edges_from(self, point: POI) -> List[Edge]:
        '''Return a list of edges that start or end at given point <point>.
        TODO: should it reverse an edge?
        '''
        edges = []
        for edge in self.edges:
            startp, endp = edge.points
            if startp.xy == point.xy:
                edges.append(edge)
            elif endp.xy == point.xy:
                edges.append(Edge(endp, startp, edge.weight))
        return edges

    def __contains__(self, target: Edge) -> bool:
        for edge in self.edges:
            if edge == target:
                return True
        return False

    def __repr__(self):
        return "<{}: edges={}>".format(self.__class__.__name__, self.edges)


class Route(Graph):
    '''A route is a subgraph, with directed edges'''

    def __init__(self, points: List[POI]):
        super().__init__()
        self.checkpoints = list(points)

    def tip(self) -> POI:
        '''Return the point at the tip of the route, which is the end point
        of the most recently added edge.
        '''
        return self.edges[-1].end

    def is_complete(self) -> bool:
        '''A route is complete is it goes through all check points'''
        # TODO: should know its expected points
        visited_points = set()
        for edge in self.edges:
            visited_points.update(edge.points)
        print("Visited", visited_points)
        not_visited = set(self.checkpoints) - visited_points
        print("Not visited", not_visited)
        return not(not_visited)

    def __copy__(self):
        newobj = type(self)(self.checkpoints)
        newobj.edges = list(self.edges)
        return newobj

    def __add__(self, other: Edge):
        if isinstance(other, Edge):
            newobj = copy.copy(self)
            newobj.edges.append(other)
            return newobj
        else:
            raise ValueError(f"Unsupported argument type: {type(other)}")
    def __len__(self) -> int:
        '''The length of a route is a sum of lengths of its segments.'''
        return sum(edge.weight for edge in self.edges)


def find_reachable_points(maze: Maze, src: POI) -> List[Edge]:
    '''In the given maze <maze>, find all points of interest that are reachable
    from the given point <src>'''
    # Starting state
    # print(maze)
    maze = copy.copy(maze)
    edges = []
    offsets = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    tips = [src]
    while tips:
        tip = tips.pop(0)
        maze[tip] = 'x'
        for dxy in offsets:
            pt = tip + dxy
            pt.distance = 1 + tip.distance
            v = maze[pt]
            # print(pt, v)
            if v == '.':
                tips.append(pt)
            elif v.isdigit():
                # point of interest reached
                endp = maze.point(v)
                # print("Endpoint", endp)
                edge = Edge(src, endp, pt.distance)
                # print(edge)
                edges.append(edge)
    return edges


def find_shortest_route(graph, maze: Maze):
    # Algorithm
    # - a route is a sequence of edges.
    # - begin at <start> point and add other points that are reachable from it.
    #   These are already graph.edges.
    #   The act of adding an edge creates a new route.
    # - allow adding the same edge (reverse route) but there should not be
    #   more that 2 of them?
    # + each route is complete if it contains all points
    # + stop for routes that are complete: do not extend them
    # + stop for routes that are longer that any existing complete route.
    start = maze.point(0)
    print("Start point", start)
    routes = [Route(maze.points) + edge for edge in graph.edges_from(start)]
    shortest_route = None
    while routes:
        curr_route = routes.pop(0)
        print("\nCurrent route:", curr_route)
        for edge in graph.edges_from(curr_route.tip()):
            if edge in curr_route:  # avoid loops
                continue
            new_route = curr_route + edge  # grow current route
            print("New route:", new_route)
            if new_route.is_complete():
                print(".. complete!")
                if not shortest_route or len(new_route) < len(shortest_route):
                    shortest_route = new_route
            elif shortest_route and len(new_route) >= len(shortest_route):
                # Stop exploring routes that are worse than the current best
                # route.
                pass
            else:
                # continue exploring this route
                routes.append(new_route)
    return shortest_route


def build_graph(maze: Maze) -> Graph:
    graph = Graph()
    for srcp in maze.points:
        print("From:", srcp)
        edges = find_reachable_points(maze, srcp)
        print(maze)
        graph.extend(edges)

    print("---- Edges ---")
    for edge in graph.edges:
        print(edge)

    for pt in maze.points:
        print("Edges from", pt)
        for edge in graph.edges_from(pt):
            print(edge)

    return graph


def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge"""
    maze = Maze.from_lines(lines)
    print("Maze has been built", maze.points)
    graph = build_graph(maze)
    best = find_shortest_route(graph, maze)
    return len(best)


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    # TODO
    return 0


text_1 = """\
###########
#0.1.....2#
#.#######.#
#4.......3#
###########\
"""

text_2 = """\
###########
#0.1....#2#
#.#.#5#.#.#
#4.......3#
###########\
"""

tests = [
    (text_1.split('\n'), 14, 0),
    (text_2.split('\n'), 16, 0),
]


def run_tests():
    print("--- Tests ---")

    for tid, (inp, exp1, exp2) in enumerate(tests):
        if exp1 is not None:
            res1 = solve_p1(inp)
            print(f"T1.{tid}:", res1 == exp1, exp1, res1)

        if exp2 is not None:
            res2 = solve_p2(inp)
            print(f"T2.{tid}:", res2 == exp2, exp2, res2)


def run_real():
    lines = utils.load_input()

    print(f"--- Day {DAY} p.1 ---")
    exp1 = -1
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {DAY} p.2 ---")
    exp2 = -1
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    # run_real()
