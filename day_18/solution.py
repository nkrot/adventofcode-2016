#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils

DAY = '18'
DEBUG = False


def digitize(s: str) -> List[int]:
    '''Convert string to list of 0s and 1s, where
    * 0 represents a trap tile ^
    * 1 represents a safe tile .
    '''
    digits = {'.': 1, '^': 0}
    return [digits[ch] for ch in list(s)]


TRAPS = [
    digitize('^^.'),
    digitize('.^^'),
    digitize('^..'),
    digitize('..^')
]


def build(prev: List[int]) -> List[int]:
    newline = []
    prev = digitize('.') + prev + digitize('.')
    for c in range(0, len(prev)-2):
        ch = '.'
        if prev[c:c+3] in TRAPS:
            ch = '^'
        newline.extend(digitize(ch))
    return newline


def solve_p1(line: str, n_lines: int) -> int:
    """Solution to the 1st part of the challenge"""
    curr = digitize(line.strip())
    cnt = sum(curr)
    for i in range(0, n_lines-1):
        curr = build(curr)
        cnt += sum(curr)
    return cnt


def solve_p2(line: str) -> int:
    """Solution to the 2nd part of the challenge"""
    return solve_p1(line, 400000)

# real 35,78; user 35,78

tests = [
    (('..^^.', 3), 6, None),
    (('.^^.^.^^^^', 10), 38, None)
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
    lines = utils.load_input()

    print(f"--- Day {DAY} p.1 ---")
    exp1 = 1987
    res1 = solve_p1(lines[0], 40)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {DAY} p.2 ---")
    exp2 = 19984714
    res2 = solve_p2(lines[0])
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
