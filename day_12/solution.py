#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List, Union
from collections import defaultdict

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils


DEBUG = False


class AssembunnyInterpreter(object):

    @staticmethod
    def parse_lines(lines: List[str]) -> List[tuple]:
        commands = []
        for line in lines:
            tokens = line.strip().split()
            if tokens:
                tokens = [int(t) if re.match(r'-?\d+$', t) else t for t in tokens]
                commands.append(tuple(tokens))
        return commands

    def __init__(self, commands: List[tuple]):
        self.commands = commands
        self.registers = {'a': 0,  'b': 0, 'c': 0, 'd': 0}
        self.debug = False
        self.pos = 0
        self.offset = 1  # jump

    def value(self, n: Union[str, int]) -> int:
        if isinstance(n, str):
            return self.registers[n]
        return n

    def cpy(self, cmd: tuple):
        self.registers[cmd[2]] = self.value(cmd[1])

    def inc(self, cmd: tuple):
        self.registers[cmd[1]] += 1

    def dec(self, cmd: tuple):
        self.registers[cmd[1]] -= 1

    def jnz(self, cmd: tuple):
        if self.value(cmd[1]):
            self.offset = self.value(cmd[2])

    def inspect(self):
        print("--- computer state --")
        print("Registers", self.registers)
        for idx, cmd in enumerate(self.commands):
            print(f"[{idx}]: {cmd}")
        print("--- END ---")

    def run(self):
        self.pos = 0
        # self.inspect()
        while self.pos < len(self.commands):
            self.offset = 1
            cmd = self.commands[self.pos]
            if self.debug:
                print("--- Before ---")
                print(self.pos, cmd)
                print("Registers", self.registers)
            meth = getattr(self, cmd[0])
            if meth:
                meth(cmd)
            else:
                raise ValueError(f"Unrecognized command: {cmd}")
            self.pos += self.offset
            if self.debug:
                print("--- After ---")
                print("Registers:", self.registers)
                print("Cursor at", self.pos)
        return self.registers

    def add(self, cmd: tuple):
        '''operation `add ARG1 TRG`'''
        self.registers[cmd[2]] = self.value(cmd[1]) + self.value(cmd[2])

    def mul(self, cmd: tuple):
        '''operation `mul ARG1 TRG`'''
        self.registers[cmd[2]] = self.value(cmd[1]) * self.value(cmd[2])

    def optimize(self):
        '''Replace some blocks with other operations.'''
        if self.debug:
            print("--- optimizing ---")
        self._rewrite_loop_as_sum()
        #self._rewrite_nested_loops_as_multiplication()

    def _rewrite_loop_as_sum(self):
        '''
        [21]: ('inc', 'a')        --> add d a     // k-th line
        [22]: ('dec', 'd')        --> cpy d 0     // l-th line
        [23]: ('jnz', 'd', -2)    --> jnz 0 0     // m-th line

        Due to this optimization, runnning time decreases:
        * user 23,97 --> 0,05
        '''

        for m, cmd_m in enumerate(self.commands):
            if m > 1 and cmd_m[0] == 'jnz' and cmd_m[2] == -2:
                # print(m, cmd_m)
                k, l = m - 2, m - 1
                cmd_k = self.commands[k]
                cmd_l = self.commands[l]
                if (cmd_k[0] == 'inc' and cmd_l[0] == 'dec'
                    and cmd_l[1] == cmd_m[1]):
                    _cmd_k = ('add', cmd_l[1], cmd_k[1])
                    _cmd_l = ('cpy', 0, cmd_l[1])
                    _cmd_m = ('jnz', 0, 0)
                    self.commands[k] = _cmd_k
                    self.commands[l] = _cmd_l
                    self.commands[m] = _cmd_m


#https://www.reddit.com/r/adventofcode/comments/5jvbzt/2016_day_23_solutions/
# optimize some constructions replacing inc/dec with multiplication

# [19]: ('cpy', 94, 'c')
# [20]: ('cpy', 80, 'd')
#   [21]: ('inc', 'a')
#   [22]: ('dec', 'd')
#   [23]: ('jnz', 'd', -2)
# [24]: ('dec', 'c')
# [25]: ('jnz', 'c', -5)


def solve_p1(lines: List[str], part=1) -> int:
    """Solution to the 1st part of the challenge"""
    commands = AssembunnyInterpreter.parse_lines(lines)
    if DEBUG:
        for i, cmd in enumerate(commands):
            print(i, cmd)

    computer = AssembunnyInterpreter(commands)
    computer.debug = DEBUG

    if part == 2:
        computer.registers['c'] = 1

    # computer.inspect()
    computer.optimize()
    # computer.inspect()
    computer.run()

    return computer.registers['a']


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    return solve_p1(lines, 2)


text_1 = """\
cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a\
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
    (text_1.split('\n'), 42, None),
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
    day = '12'
    lines = utils.load_input()

    print(f"--- Day {day} p.1 ---")
    exp1 = 318009
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {day} p.2 ---")
    exp2 = 9227663
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
