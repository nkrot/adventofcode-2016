#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List, Tuple

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils


DEBUG = False

# x is horizontal, y is vertical
OFFSETS = [(0, -1), (1, 0), (0, 1), (-1, 0)]


def around(pt: Tuple[int, int]):
    for dx, dy in OFFSETS:
        x = pt[0] + dx
        y = pt[1] + dy
        if x > -1 and y > -1:
            yield((x, y))


def is_wall(loc, favnum):
    x, y = loc
    s = (x+y) ** 2 + 3*x + y + favnum
    return bool(f'{s:b}'.count('1') % 2)


def solve_p1(target, favnum, part=1) -> int:
    """Solution to the 1st part of the challenge"""

    origin = (1, 1)
    maze = {origin: 0}

    # perform BFS-like exploration of the maze
    queue = [origin]
    while queue:
        curr_loc = queue.pop(0)

        if part == 2 and maze[curr_loc] == 50:
            # how many locations are 50 steps away from the origin
            return sum(1 for dist in maze.values() if dist > -1)

        for near_loc in around(curr_loc):
            if near_loc in maze:
                # ignore visited locations
                continue

            # print(near_loc)
            if is_wall(near_loc, favnum):
                maze[near_loc] = -1
                continue

            maze[near_loc] = 1 + maze[curr_loc]
            if part == 1 and near_loc == target:
                return maze[near_loc]

            queue.append(near_loc)

    return 0


def solve_p2(*args) -> int:
    """Solution to the 2nd part of the challenge"""
    return solve_p1(*args, 2)


tests = [
    (((7, 4), 10), 11, None),
]


def run_tests():
    print("--- Tests ---")

    for tid, (inp, exp1, exp2) in enumerate(tests):
        if exp1 is not None:
            res1 = solve_p1(*inp)
            print(f"T1.{tid}:", res1 == exp1, exp1, res1)

        if exp2 is not None:
            res2 = solve_p2(inp)
            print(f"T2.{tid}:", res2 == exp2, exp2, res2)


def run_real():
    day = '13'
    inp = ((31, 39), 1362)

    print(f"--- Day {day} p.1 ---")
    exp1 = 82
    res1 = solve_p1(*inp)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {day} p.2 ---")
    exp2 = 138
    res2 = solve_p2(*inp)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
