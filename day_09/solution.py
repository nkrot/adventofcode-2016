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


def decode(line: str) -> str:
    if DEBUG:
        print(f"Decoding: {line}")
    decoded = ''
    while line:
        m = re.match(r'\((\d+)x(\d+)\)', line)
        if m:
            length, nreps = int(m.group(1)), int(m.group(2))
            line = line[m.end():]
            decoded += line[:length] * nreps
            line = line[length:]
        else:
            decoded += line[0]
            line = line[1:]
    if DEBUG:
        print(decoded)
    return decoded


def decode2(line: str) -> int:
    # ex: X(8x2)(3x3)ABCY -> XABCABCABCABCABCABCY
    # X (8x2)(3x3)ABC Y
    # X (3x3)ABC(3x3)ABC Y
    # X ABC ABC ABC ABC ABC ABC Y
    decoded_length = 0
    while line:
        m = re.match(r'\((\d+)x(\d+)\)', line)
        if m:
            length, nreps = int(m.group(1)), int(m.group(2))
            line = line[m.end():]  # current marker removed
            # This works because there are no overlapping markers.
            # In other words, markers and data work like composition
            # of functions.
            decoded_length += decode2(line[:length]) * nreps
            line = line[length:]
        else:
            decoded_length += 1
            line = line[1:]
    return decoded_length


def solve_p1(lines: List[str], part=1) -> int:
    """Solution to the 1st part of the challenge"""
    decoded = [decode(line) for line in lines]
    if part == 0:
        return decoded
    elif part == 1:
        return sum([len(line) for line in decoded])
    return 0


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    decoded = [decode2(line) for line in lines]
    return sum(decoded)


tests = [
    (['ADVENT'],
     ['ADVENT'], None),
    (['A(1x5)BC'],
     ['ABBBBBC'], None),
    (['(3x3)XYZ'],
     ['XYZXYZXYZ'], None),
    (['A(2x2)BCD(2x2)EFG'],
     ['ABCBCDEFEFG'], None),
    (['(6x1)(1x3)A'],
     ['(1x3)A'], None),
    (['X(8x2)(3x3)ABCY'],
     ['X(3x3)ABC(3x3)ABCY'], None),

    (['(3x3)XYZ'], None, len('XYZXYZXYZ')),
    (['X(8x2)(3x3)ABCY'], None, len('XABCABCABCABCABCABCY')),
    (['(27x12)(20x12)(13x14)(7x10)(1x12)A'], None, 241920),
    (['(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN'],
     None, 445)
]


def run_tests():
    print("--- Tests ---")

    for tid, (inp, exp1, exp2) in enumerate(tests):
        if exp1 is not None:
            res1 = solve_p1(inp, part=0)
            print(f"T1.{tid}:", res1 == exp1, exp1, res1)

        if exp2 is not None:
            res2 = solve_p2(inp)
            print(f"T2.{tid}:", res2 == exp2, exp2, res2)


def run_real():
    day = '09'
    lines = utils.load_input()

    print(f"--- Day {day} p.1 ---")
    exp1 = 123908
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {day} p.2 ---")
    exp2 = 10755693147
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
