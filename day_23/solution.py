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
from day_12.solution import AssembunnyInterpreter as BaseInterpreter


DAY = '23'
DEBUG = False


class AssembunnyInterpreter(BaseInterpreter):
    '''Introduces a new operation `tgl`'''

    def tgl(self, cmd: tuple):
        print("Hello from tgl", cmd)
        arg = self.dereference(cmd[1])
        pos = self.pos + arg
        if pos < len(self.commands):
            other_cmd = self.commands[pos]
            if self.debug:
                print("Rewriting", pos, other_cmd)
            if len(other_cmd) == 2:
                # ex: For one-argument instructions, inc becomes dec, and all
                # other one-argument instructions become inc.
                if other_cmd[0] == 'inc':
                    self.commands[pos] = ('dec', other_cmd[1])
                else:
                    self.commands[pos] = ('inc', other_cmd[1])
            if len(other_cmd) == 3:
                # For two-argument instructions, jnz becomes cpy, and all other
                # two-instructions become jnz.
                if other_cmd[0] == 'jnz':
                    self.commands[pos] = ('cpy',) + other_cmd[1:]
                else:
                    self.commands[pos] = ('jnz',) + other_cmd[1:]
            if self.debug:
                print("Rewritten", self.commands[pos])
        self.inspect()


def solve_p1(lines: List[str], part: int = 0) -> int:
    """Solution to the 1st part of the challenge"""
    commands = AssembunnyInterpreter.parse_lines(lines)
    if DEBUG:
        for i, cmd in enumerate(commands):
            print(i, cmd)

    computer = AssembunnyInterpreter(commands)
    computer.debug = DEBUG
    if part == 1:
        computer.registers['a'] = 7
    elif part == 2:
        computer.registers['a'] = 12

    computer.run()

    return computer.registers['a']


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    return solve_p1(lines, 2)


text_1 = """cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a
"""


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

    # print(f"--- Day {DAY} p.1 ---")
    # exp1 = 12560
    # res1 = solve_p1(lines, 1)
    # print(exp1 == res1, exp1, res1)

    print(f"--- Day {DAY} p.2 ---")
    exp2 = -1
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
