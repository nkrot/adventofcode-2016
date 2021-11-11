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

    def dereference(self, n: Union[str, int]) -> int:
        if isinstance(n, str):
            return self.registers[n]
        return n

    def run(self):
        pos = 0
        while pos < len(self.commands):
            offset = 1
            cmd = self.commands[pos]
            if DEBUG:
                print(pos, cmd)
                print(self.registers)
            if cmd[0] == 'cpy':
                self.registers[cmd[2]] = self.dereference(cmd[1])
            elif cmd[0] == 'inc':
                self.registers[cmd[1]] += 1
            elif cmd[0] == 'dec':
                self.registers[cmd[1]] -= 1
            elif cmd[0] == 'jnz':
                if self.dereference(cmd[1]):
                    offset = cmd[2]
            else:
                raise ValueError(f"Unrecognized command: {cmd}")
            pos += offset
            if self.debug:
                print(self.registers)
                print(pos)


def solve_p1(lines: List[str], part=1) -> int:
    """Solution to the 1st part of the challenge"""
    commands = AssembunnyInterpreter.parse_lines(lines)
    if DEBUG:
        for i, cmd in enumerate(commands):
            print(i, cmd)

    computer = AssembunnyInterpreter(commands)

    if part == 2:
        computer.registers['c'] = 1

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


tests = [
    (text_1.split('\n'), 42, None),
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
