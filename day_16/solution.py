#!/usr/bin/env python

# # #
# The solution implemented is straightforward and will probably fail for
# larger disk sizes.
# Is there a way to avoid generating the whole string?
#

import re
import os
import sys
from typing import List

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils


DEBUG = False


def extend(a: str, maxlen=20) -> str:
    while len(a) < maxlen:
        bs = ['0' if ch == '1' else '1' for ch in list(a)]
        a = a + '0' + ''.join(reversed(bs))
        # print(len(a), a)
    return a[0:maxlen]


def checksum(s: str):
    while True:
        chks = ''
        for i in range(0, len(s)-1, 2):
            j = i + 1
            # print(i, j, s[i], s[j])
            chks += '1' if s[i] == s[j] else '0'
        # print(chks)
        if len(chks) % 2:
            break
        s = chks
    return chks


print(extend('10000', 20) == '10000011110010000111')
print(checksum('110010110100') == '100')
print(checksum('10000011110010000111') == '01100')


def solve_p1(seed: str, maxlen: int) -> str:
    """Solution to the 1st part of the challenge"""
    return checksum(extend(seed, maxlen))


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    # TODO
    return 0


tests = [
    (('10000', 20), '01100', None),
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
    day = '16'
    inp = "11011110011011101"

    print(f"--- Day {day} p.1 ---")
    exp1 = '00000100100001100'
    res1 = solve_p1(inp, 272)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {day} p.2 ---")
    exp2 = '00011010100010010'
    res2 = solve_p1(inp, 35651584)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
