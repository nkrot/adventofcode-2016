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


DEBUG = False


class Disc(object):

    @classmethod
    def from_text(cls, line: str):
        obj = cls(*re.findall(r'\d+', line))
        return obj

    def __init__(self, id, period, time=0, start=0):
        self.id = int(id)
        self.period = int(period)
        self.time = int(time)
        self.start = int(start)
        if self.id > self.period:
            self.target = self.period - (self.id % self.period)
        else:
            self.target = self.period - self.id
        assert self.target > -1, f"Wrong value of target: {self.target}"
        self.position = self.start

    def spin(self, t: int) -> bool:
        '''Move the disc in the state that corresponds to given time <t>'''
        self.time = t
        self.position = (self.start + self.time) % self.period
        return self.position == self.target

    def __repr__(self):
        return "<{}: id={}, start={}, period={}, target={}: ({}, {})>".format(
            self.__class__.__name__, self.id, self.start,
            self.period, self.target,
            self.time, self.position)


def solve1(discs: List[Disc]) -> int:
    '''Naive implementation'''

    if DEBUG:
        print("--- Initial state --")
        for d in discs:
            print(d)

    t = 1
    while not all(d.spin(t) for d in discs):
        t += 1

    if DEBUG:
        print(f"--- Final state at time {t} --")
        for d in discs:
            # print(f"--- {d.id} ---")
            # print(d)
            d.spin(d.time + d.id)
            print(d)

    return t

# solve1:
# - real 7,34; user 7,27 (with all(list) )
# - real 2,47; user 2,42 (with all(generator) ). wow!
#
# solve2:
# - real 0,04; user 0,02
#
# With the optimization, number of iterations changed drastically:
#      | solve1  | solve2 |
# T1.0 | 4       | 1      |
# p.1  | 400588  | 17     |
# p.2  | 3045958 | 25     |


def solve2(discs) -> int:
    '''
    t step is modified based on the cases that have been solved so far
    For example, if as soon as we found t_x that brings a disc into target
    state, we need to check time ticks only that are devisible by t_x.
    We update the increment correspondingly.
    '''

    # Choose starting point
    # - disc with the longest period;
    # - start from time tick t that corresponds to the target state. there is
    #   no need to check previous time ticks.
    discs = sorted(discs, key=lambda d: -d.period)
    disc = discs[0]
    t = disc.target - disc.start

    incr = 1
    n = 0

    if DEBUG:
        print(f"Start at {t} with disc {disc}")

    for i in range(0, len(discs)):
        disc = discs[i]
        while not disc.spin(t):
            n += 1
            t += incr
        if DEBUG:
            print(i, incr, n, disc)
        incr *= disc.period

    print(f"Iterations: {n}")

    # check
    assert all(disc.spin(t) for d in discs), "Not solved"

    return t


def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge"""
    discs = [Disc.from_text(line) for line in lines if line]
    # return solve1(discs)
    return solve2(discs)


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    discs = [Disc.from_text(line) for line in lines if line]
    discs.append(Disc(discs[-1].id+1, 11, 0, 0))
    # return solve1(discs)
    return solve2(discs)


text_1 = """\
Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1.
"""

text_2 = """\
Disc #3 has 3 positions; at time=0, it is at position 0.
Disc #4 has 4 positions; at time=0, it is at position 2.
Disc #5 has 2 positions; at time=0, it is at position 0.
"""


tests = [
    (text_1.split('\n'), 5, None),
    # (text_2.split('\n'), 4, None),
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
    day = '15'
    lines = utils.load_input()

    print(f"--- Day {day} p.1 ---")
    exp1 = 400589
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {day} p.2 ---")
    exp2 = 3045959
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
