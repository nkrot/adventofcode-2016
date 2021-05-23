#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List, Tuple
from hashlib import md5

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils


DEBUG = False
T_COORD = Tuple[int, int]


MAZEMAP = """\
#########
#S| | | #
#-#-#-#-#
# | | | #
#-#-#-#-#
# | | | #
#-#-#-#-#
# | | |
####### V"""


class Maze(object):

    OFFSETS = {
        'U': (-1, 0),
        'D': (+1, 0),
        'L': (0, -1),
        'R': (0, +1)
    }

    def __init__(self):
        # x is vertical axis, y is horizontal axis
        self.shape = (4, 4)
        self.start = (0, 0)  # (x, y) of top left (S)
        self.exit  = (3, 3)  # (x, y) of bottom right

    def open_doors(self, passcode: str, loc: T_COORD):
        '''List doors that open from the given position <loc>'''
        hdg = md5(passcode.encode()).hexdigest()
        states = [ch in 'bcdef' for ch in hdg[0:4]]
        for direction, is_open in zip(list('UDLR'), states):
            newloc = self._position(loc, direction)
            if is_open and newloc in self:
                yield(direction, newloc)

    def __contains__(self, xy: T_COORD) -> bool:
        '''Tell if given coordinate is within the maze'''
        return 0 <= xy[0] < self.shape[0] and 0 <= xy[1] < self.shape[1]

    def _position(self, xy: T_COORD, direction: str) -> T_COORD:
        d = direction.upper()
        x = xy[0] + self.OFFSETS[d][0]
        y = xy[1] + self.OFFSETS[d][1]
        return (x, y)


def bfs(basecode: str, maze: Maze, part=1):
    '''
    - Part 1: BFS finds the shortest path first
    - Part 2: DFS would more efficient in terms of memory but with small search
      space, why bother :)
    '''

    longest = None  # for part 2
    routes = [(maze.start, '')]
    while routes:
        loc, path = routes.pop(0)
        passcode = basecode + path
        for direction, newloc in maze.open_doors(passcode, loc):
            newroute = (newloc, path + direction)
            if newloc == maze.exit:
                if part == 2:
                    #solutions.append(newroute)
                    # the last one found is the one with longest path
                    longest = newroute
                else:
                    # the 1st solution is the shortest one
                    return newroute[-1]
            else:
                routes.append(newroute)

    if part == 2:
        #return max(len(sol[-1]) for sol in solutions)
        return len(longest[-1])


def solve_p1(passcode: str) -> str:
    """Solution to the 1st part of the challenge"""
    return bfs(passcode, Maze(), 1)


def solve_p2(passcode: str) -> int:
    """Solution to the 2nd part of the challenge"""
    return bfs(passcode, Maze(), 2)


tests = [
    ("hijkl", '', None),
    ('ihgpwlah', 'DDRRRD', 370),
    ('kglvqrro', 'DDUDRLRRUDRD', 492),
    ('ulqzkmiv', 'DRURDRUDDLLDLUURRDULRLDUUDDDRR', 830)
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
    day = '17'
    inp = 'pslxynzg'

    print(f"--- Day {day} p.1 ---")
    exp1 = 'DDRRUDLRRD'
    res1 = solve_p1(inp)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {day} p.2 ---")
    exp2 = 488
    res2 = solve_p2(inp)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
