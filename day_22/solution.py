#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List, Tuple
from dataclasses import dataclass

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils

DAY = '22'
DEBUG = False


@dataclass
class Node:

    name:  str = None
    size:  int = 0  # T
    used:  int = 0  # T
    avail: int = 0  # T
    use:   int = 0  # %
    pos:   Tuple[int, int] = (-1, -1)

    @classmethod
    def parse_text(cls, line: str):
        node = None
        if line.startswith('/dev/'):
            fields = line.strip().split()
            for i in range(1, len(fields)):
                fields[i] = int(fields[i][:-1])
            node = cls(*fields)
            m = re.search(r'x(\d+)-y(\d+)', node.name)
            node.pos = (int(m.group(1)), int(m.group(2)))
        return node

    @property
    def x(self):
        return self.pos[0]

    @property
    def y(self):
        return self.pos[1]


def visualize(nodes: List[Node]):
    max_x = max(n.x for n in nodes) + 1
    max_y = max(n.y for n in nodes) + 1

    mat = [['.'] * max_y for r in range(max_x)]
    for n in nodes:
        mat[n.x][n.y] = '+'

    print('\n'.join(''.join(r) for r in mat))


def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge"""
    nodes = [Node.parse_text(line) for line in lines
             if line.startswith('/dev')]

    if DEBUG:
        visualize(nodes)  # looks like all nots are reachabe any other node

    c = 0
    for v in nodes:
        if not v.used:
            continue
        for w in nodes:
            if v.used <= w.avail and w.name != v.name:
                c += 1
    return c


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    # TODO
    return 0


tests = []


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
    exp1 = 967
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {DAY} p.2 ---")
    exp2 = -1
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    # run_tests()
    run_real()
