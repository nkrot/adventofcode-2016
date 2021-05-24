#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils

DAY = '19'
DEBUG = False

def solve_p1_naive(n_elves):
    elves = np.ones(n_elves)
    if DEBUG:
        print(elves)

    r = 0
    take = False
    while sum(elves) > 1:
        r += 1
        if DEBUG:
            print(f"Round #{r}")
        for i in range(0, n_elves):
            if elves[i]:
                if take:
                    elves[i] = 0
                take = not take
        if DEBUG:
            print(elves)

    idxs = np.where(elves==1)[0]
    assert len(idxs) == 1, "OOps"

    return idxs[0]+1


def solve_p1_v2(n_elves: int) -> int:
    # TODO: does not work

    start = 1
    step = 2

    r = 0
    while n_elves / step > 2:
        r += 1
        print(f"Round #{r} start={start} step={step}")
        if n_elves % step:
            start += step
        step *= 2

    return start


def solve_p2_naive(n_elves: int) -> int:
    '''TODO: sucks'''
    elves = np.array(range(1, 1+n_elves))

    # print(elves)
    i = 0
    while len(elves) > 1:
        incr = 1
        if i % 2: # odd
            victim = len(elves) // 2 + i - 1
        else: # even
            victim = len(elves) // 2 + i
        if victim >= len(elves):
            victim %= len(elves)
            incr = 0
        print(i, elves[i], victim, elves[victim], elves)
        elves = np.delete(elves, [victim])
        print("-->", elves)
        i += incr
        if i == len(elves):
            i = 0

    return elves[0]


def solve_p1(n_elves: int) -> int:
    """Solution to the 1st part of the challenge"""
    return solve_p1_naive(n_elves)


def solve_p2(n_elves) -> int:
    """Solution to the 2nd part of the challenge"""
    return solve_p2_naive(n_elves)



tests = [
    (5, 3, 2),
    (22, 13, 17),
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
    inp = 3012210

    print(f"--- Day {DAY} p.1 ---")
    # exp1 = 1830117
    # res1 = solve_p1(inp)
    # print(exp1 == res1, exp1, res1)

    print(f"--- Day {DAY} p.2 ---")
    exp2 = -1
    res2 = solve_p2(inp)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    # run_real()
