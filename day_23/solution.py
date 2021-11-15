#!/usr/bin/env python

# # #
#
# The 2nd part runs quite a long time. To improve performance,  use pypy
# > time -p pypy3 solution.py
#    user 176,21
# Alternatively, implement optimization (search below for ideas).


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
        arg = self.value(cmd[1])
        pos = self.pos + arg
        # print(cmd, "modifies line", pos)
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
        # self.inspect()

    def add(self, cmd: tuple):
        '''operation `add ARG1 TRG`'''
        self.registers[cmd[2]] = self.value(cmd[1]) + self.value(cmd[2])

    def mul(self, cmd: tuple):
        '''operation `mul ARG1 TRG`'''
        self.registers[cmd[2]] = self.value(cmd[1]) * self.value(cmd[2])

    def optimize(self):
        '''Replace some blocks with other operations.

        This however should be done carefully, as `tgl` instruction may affect
        rewritten code. Perhaps, rewritten section should remain active for as
        long as the execution is within the section, and restored to
        the original state otherwise.
        '''
        self._rewrite_loop_as_sum()
        #self._rewrite_nested_loops_as_multiplication()

    def _rewrite_loop_as_sum(self):
        '''
        [21]: ('inc', 'a')        --> add d a
        [22]: ('dec', 'd')        --> cpy d 0
        [23]: ('jnz', 'd', -2)    --> jnz 0 0
        '''
        raise NotImplementedError("Worth trying...")


#https://www.reddit.com/r/adventofcode/comments/5jvbzt/2016_day_23_solutions/
# optimize some constructions replacing inc/dec with multiplication

# [19]: ('cpy', 94, 'c')
# [20]: ('cpy', 80, 'd')
#   [21]: ('inc', 'a')
#   [22]: ('dec', 'd')
#   [23]: ('jnz', 'd', -2)
# [24]: ('dec', 'c')
# [25]: ('jnz', 'c', -5)

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

# my own additional operators, to be used in optimized code

text_2 = """cpy 2 a
cpy 3 b
add b a
add 10 a
"""

text_3 = """cpy 2 a
cpy 3 b
add b a
mul 10 a
"""

tests = [
    (text_1.split('\n'), 3, None),
    (text_2.split('\n'), 15, None),
    (text_3.split('\n'), 50, None),
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
    exp1 = 12560
    res1 = solve_p1(lines, 1)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {DAY} p.2 ---")
    exp2 = 479009120 # takes forever w/o optimization
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
