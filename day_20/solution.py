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

DAY = '20'
DEBUG = False


def parse(lines: List[str]):
    ranges = [list(map(int, line.strip().split('-')))
              for line in lines if line]
    return ranges


def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge"""
    ranges = sorted(parse(lines))
    # print(ranges)
    for i in range(1, len(ranges)):
        p, c = ranges[i-1], ranges[i]
        if p[-1]+1 < c[0]:
            return p[-1]+1
    return 0


IPS = [0, 4294967295]


def merge(ranges: List[List[int]]) -> List[List[int]]:
    merged = [[0, 0]]

    for curr in sorted(ranges):
        prev = merged[-1]
        if curr[0] - prev[1] > 1:
            # non overlapping ranges
            merged.append(curr)
        elif prev[1] < curr[1]:
            # extend previous range to include current range
            prev[1] = curr[1]

    return merged


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    ranges = merge(parse(lines))
    # print(ranges)
    nmax = IPS[1] - IPS[0] + 1
    for b, e in ranges:
        nmax -= (e - b + 1)
        # print(b, e)
    return nmax


text_1 = """5-8
0-2
4-7"""


tests = [
    (text_1.split('\n'), 3, None),
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
    exp1 = 32259706
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {DAY} p.2 ---")
    exp2 = 113
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
