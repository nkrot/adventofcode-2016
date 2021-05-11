#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
import pandas as pd
from typing import List


sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils


DEBUG = False


def solve_p1(lines: List[str], pos=0) -> int:
    """Solution to the 1st part of the challenge"""
    rows = [list(line) for line in lines]
    df = pd.DataFrame(rows)
    most_frequent = df.agg(lambda x: x.value_counts().index[pos])
    return ''.join(most_frequent.values)


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    return solve_p1(lines, -1)


text_1 = """eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar"""


tests = [
    (text_1.split('\n'), 'easter', 'advent'),
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
    day = '06'
    lines = utils.load_input()

    print(f"--- Day {day} p.1 ---")
    exp1 = 'afwlyyyq'
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {day} p.2 ---")
    exp2 = 'bhkzekao'
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
