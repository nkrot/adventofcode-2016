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


class Keypad(object):

    OFFSETS = {
        'U': (-1, 0),
        'D': (+1, 0),
        'R': (0, +1),
        'L': (0, -1)
    }

    def __init__(self):
        self.buttons = ["123", "456", "789"]
        self.position = (1, 1)

    @property
    def buttons(self):
        return self._buttons

    @buttons.setter
    def buttons(self, rows: List[str]):
        self._buttons = []
        for row in rows:
            self._buttons.append(list(row))
        self.shape = (len(self._buttons), len(self._buttons[0]))

    def key(self) -> str:
        '''Return the key at current position'''
        row, col = self.position
        return self.buttons[row][col]

    def move(self, instr: str) -> bool:
        '''Move current position according to the instruction'''
        assert instr in self.OFFSETS.keys(), f'Invalid instruction: {instr}'
        ok = False
        offset = self.OFFSETS[instr]
        nrow, ncol = [self.position[i] + offset[i]
                      for i in range(len(self.position))]
        if (0 <= nrow < self.shape[0]
              and 0 <= ncol < self.shape[1]
              and self.buttons[nrow][ncol] is not None):
            self.position = (nrow, ncol)
            ok = True
        return ok


def solve_p1(lines: List[str], kpad = None) -> str:
    """Solution to the 1st part of the challenge"""
    codes = []
    keypad = kpad or Keypad()
    for line in lines:
        for ch in line.strip():
            keypad.move(ch)
        codes.append(keypad.key())
    return ''.join(codes)


def solve_p2(lines: List[str]) -> str:
    """Solution to the 2nd part of the challenge"""
    keypad = Keypad()
    keypad.buttons = [
        [None, None, "1", None, None],
        [None,  "2", "3",  "4", None],
        [  "5", "6", "7",  "8",  "9"],
        [None,  "A", "B",  "C", None],
        [None, None, "D", None, None],
    ]
    keypad.position = (2, 0)  # at 5
    return solve_p1(lines, keypad)


text_1 = """ULL
RRDDD
LURDL
UUUUD"""


tests = [
    (text_1.split('\n'), "1985", "5DB3"),
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
    day = '02'
    lines = utils.load_input()

    print(f"--- Day {day} p.1 ---")
    exp1 = '78985'
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {day} p.2 ---")
    exp2 = '57DD8'
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
