#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List
from collections import deque

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils


DEBUG = False

def is_valid_triangle(sides: list) -> bool:
    sides = deque(int(s) for s in sides)
    xxx = [list(sides)]
    for _ in range(2):
        sides.rotate(1)
        xxx.append(list(sides))
    checks = [sides[0] < sum(sides[1:]) for sides in zip(*xxx)]
    return all(checks)


def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge."""
    checks = [is_valid_triangle(line.split()) for line in lines]
    return checks.count(True)


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge.
    One triangle is three consecutive numbers in each column."""
    numbers = []
    for line in lines:
        numbers.extend(line.split())
    checks = []
    for s in range(0, len(numbers), 9):
        # 9 elements is three lines forming a square of shape (3, 3):
        # a1 a2 a3
        # b1 b2 b3
        # c1 c2 c3
        three = numbers[s:s+9]
        for i in range(3):
            # selecting 3 times with step 3 gives us triangles made of columns
            # => a1 b1 c1  -- from the 1st column
            # => a2 b2 c2  -- from the 2nd column
            # => a3 b3 c3  -- from the 3rd column
            checks.append(is_valid_triangle(three[i::3]))
    return checks.count(True)


tests = [
    (["5 10 25"], 0, None),
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
    day = '03'
    lines = utils.load_input()

    print(f"--- Day {day} p.1 ---")
    exp1 = 862
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {day} p.2 ---")
    exp2 = 1577
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
