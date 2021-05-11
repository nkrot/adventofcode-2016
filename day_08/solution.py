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


np.set_printoptions(linewidth=10000)
DEBUG = False


class Command(object):

    def __init__(self, descr):
        self.description = descr.strip()
        self.name = None
        self.args = []
        self._parse_description()

    def _parse_description(self):
        '''
        Examples:
        rect 3x2                  --> rect,      width, height
        rotate column x=1 by 1    --> rotate column, 1, 1,
        rotate row y=0 by 4       --> rotate row,    0, 4
        '''
        regexen= [
            re.compile(r'(rect)\s(\d+)x(\d+)$'),
            re.compile(r'(rotate\s(?:column|row))\s[xy]=(\d+)\sby\s(\d+)$')
        ]
        for regexp in regexen:
            m = re.match(regexp, self.description)
            if m:
                self.name = m.group(1)
                self.args = tuple(int(v) for v in m.group(2, 3))

    def __repr__(self):
        return "<{}: name={}, args={}>".format(
            self.__class__.__name__, self.name, self.args)


class Screen(object):

    GRAPHICS = {0: '.', 1: '#'}

    def __init__(self, size=(50, 6)):
        self.width, self.height = size  # (x, y)
        self.data = np.zeros((self.height, self.width), dtype=np.int8)

    def execute(self, cmd: Command):
        if cmd.name == 'rect':
            w, h = cmd.args
            self.data[:h,:w] = 1
        elif cmd.name == 'rotate column':
            c, s = cmd.args
            self.data[:,c] = np.roll(self.data[:,c], s)
        elif cmd.name == 'rotate row':
            r, s = cmd.args
            self.data[r,:] = np.roll(self.data[r,:], s)

    def number_of_lit_pixels(self):
        return self.data.sum()

    def __str__(self):
        lines = []
        for r in range(self.height):
            chars = [self.GRAPHICS[v] for v in self.data[r,:]]
            lines.append(''.join(chars))
        return '\n'.join(lines)


def solve_p1(lines: List[str], size=(50, 6), part=1) -> int:
    """Solution to the 1st part of the challenge"""
    commands = [Command(line) for line in lines]
    screen = Screen(size)
    if DEBUG:
        print(screen.data)
    for cmd in commands:
        if DEBUG:
            print(f'Executing: {cmd}')
        screen.execute(cmd)
        if DEBUG:
            print(screen.data)
    if part == 1:
        return screen.number_of_lit_pixels()
    elif part == 2:
        return str(screen)


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    return solve_p1(lines, (50, 6), 2)


text_1 = """rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1"""


tests = [
    (text_1.split('\n'), 6, None),
]


def run_tests():
    print("--- Tests ---")

    for tid, (inp, exp1, exp2) in enumerate(tests):
        if exp1 is not None:
            res1 = solve_p1(inp, (7, 3))
            print(f"T1.{tid}:", res1 == exp1, exp1, res1)

        if exp2 is not None:
            res2 = solve_p2(inp)
            print(f"T2.{tid}:", res2 == exp2, exp2, res2)


def run_real():
    day = '08'
    lines = utils.load_input()

    print(f"--- Day {day} p.1 ---")
    exp1 = 128
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {day} p.2 ---")
    # EOARGPHYAO
    exp2 = """\
####..##...##..###...##..###..#..#.#...#.##...##..
#....#..#.#..#.#..#.#..#.#..#.#..#.#...##..#.#..#.
###..#..#.#..#.#..#.#....#..#.####..#.#.#..#.#..#.
#....#..#.####.###..#.##.###..#..#...#..####.#..#.
#....#..#.#..#.#.#..#..#.#....#..#...#..#..#.#..#.
####..##..#..#.#..#..###.#....#..#...#..#..#..##.."""
    res2 = solve_p2(lines)
    print("{} Expected:\n{}\nGot:\n{}".format(exp2 == res2, exp2, res2))


if __name__ == '__main__':
    run_tests()
    run_real()
