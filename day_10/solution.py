#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List
from collections import defaultdict
from functools import reduce

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils


DEBUG = False


class Bin(object):

    def __init__(self, id=None):
        self.id = id
        self.chips = set()

    def add(self, chip: int):
        self.chips.add(int(chip))

    def __contains__(self, chips):
        return sorted(self.chips) == sorted(chips)

    def __repr__(self):
        return "<{}: id={} chips={}>".format(
            self.__class__.__name__, self.id, sorted(self.chips))


class Bot(Bin):

    def __init__(self, *args):
        super().__init__(*args)
        self.low = None
        self.high = None

    def execute(self) -> bool:
        '''Return status indicates whether the bot performed an action or not
        '''
        status = False
        if len(self.chips) == 2:
            chips = sorted(self.chips)
            self.low.add(chips[0])
            self.high.add(chips[1])
            self.chips.clear()
            status = True
        return status

    def __repr__(self):
        return "<{}: id={}, chips={}, low={}, high={}>".format(
            self.__class__.__name__, self.id, sorted(self.chips),
            (self.low.__class__.__name__, self.low.id),
            (self.high.__class__.__name__, self.high.id))


def setup_botnet(lines: List[str]) -> dict:
    '''Create nwtwork of Bots and output bits according to the instructions
    in <lines>.
    '''
    nodes = {'bot': {}, 'output': {}}

    def find_or_create(id, category: str = 'bot'):
        id = int(id)
        if category == 'bot':
            return nodes['bot'].setdefault(id, Bot(id))
        elif category == 'output':
            return nodes['output'].setdefault(id, Bin(id))
        raise ValueError('Shit happened')

    for line in lines:
        if DEBUG:
            print(f"Executing: {line}")

        m = re.match(r'value (\d+) goes to bot (\d+)', line)
        if m:
            node = find_or_create(m.group(2), "bot")
            node.add(m.group(1))

        m = re.match(r'bot (\d+) gives', line)
        if m:
            node = find_or_create(m.group(1), 'bot')

            for m in re.finditer(r'(low|high) to (bot|output) (\d+)', line):
                trg = find_or_create(m.group(3), m.group(2))
                setattr(node, m.group(1), trg)

    if DEBUG:
        print(nodes)

    return nodes


def solve_p1(lines: List[str], chips) -> int:
    nodes = setup_botnet(lines)

    keep_going = True
    while keep_going:
        keep_going = False
        for bot in nodes['bot'].values():
            if chips and chips in bot:
                return bot.id   # part 1
            keep_going = bot.execute() or keep_going

    return nodes  # part 2


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    nodes = solve_p1(lines, None)
    values = []
    for idx in [0, 1, 2]:
        values.extend(nodes['output'][idx].chips)
    return reduce(lambda a, b: a*b, values, 1)


text_1 = """\
value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2"""


tests = [
    (text_1.split('\n'), [2, (2, 5)], None),
]


def run_tests():
    print("--- Tests ---")

    for tid, (inp, (exp1, chips), exp2) in enumerate(tests):
        if exp1 is not None:
            res1 = solve_p1(inp, chips)
            print(f"T1.{tid}:", res1 == exp1, exp1, res1)

        if exp2 is not None:
            res2 = solve_p2(inp)
            print(f"T2.{tid}:", res2 == exp2, exp2, res2)


def run_real():
    day = '10'
    lines = utils.load_input()

    print(f"--- Day {day} p.1 ---")
    exp1 = 98
    res1 = solve_p1(lines, (61, 17))
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {day} p.2 ---")
    exp2 = 4042
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
