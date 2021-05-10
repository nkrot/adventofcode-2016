#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List
from collections import Counter

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils


DEBUG = False

class Room(object):
    '''
    code: aaaaa-bbb-z-y-x-123[abxyz]
    - an encrypted name (lowercase letters separated by dashes) followed by a dash
    - a sector ID
    - a checksum in square brackets.
    '''

    def __init__(self, code):
        m = re.match(r'([a-z-]+)-(\d+)\[([a-z]+)\]$', code.strip())
        self.name = m.group(1)
        self.sector_id = int(m.group(2))
        self.checksum = m.group(3)

    def is_valid(self) -> bool:
        counts = Counter(self.name.replace('-', ''))
        by_counts = [[] for _ in range(len(self.name))]
        for ch, cnt in counts.most_common():
            by_counts[cnt].append(ch)
        chars = [] # arranged by length and within each length, alphabetically
        for groups in reversed(by_counts):
            chars.extend(sorted(groups))
        return "".join(chars).startswith(self.checksum)


class ShiftCipher(object):

    ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

    @classmethod
    def decode(cls, room: Room) -> str:
        shift = room.sector_id % len(cls.ALPHABET)
        shifted_alphabet = cls.ALPHABET[shift:] + cls.ALPHABET[0:shift]
        chars = []
        for ch in room.name:
            if ch == '-':
                chars.append(' ')
            elif ch in cls.ALPHABET:
                pos = cls.ALPHABET.index(ch)
                chars.append(shifted_alphabet[pos])
            else:
                raise ValueError(f'Invalid character: {ch}')
        return "".join(chars)


def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge"""
    rooms = [Room(line) for line in lines]
    valid_rooms = [room.sector_id for room in rooms if room.is_valid()]
    return sum(valid_rooms)


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    for line in lines:
        room = Room(line)
        if room.is_valid():
            name = ShiftCipher.decode(room).lower()
            if re.match(r'north\s*pole\s*object', name):
                return room.sector_id
    return 0


text_1 = """aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]"""


tests = [
    (text_1.split('\n'), 1514, None),
    #(["qzmt-zixmtkozy-ivhz-343[zimth]"], None, "very encrypted name")
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
    day = '04'
    lines = utils.load_input()

    print(f"--- Day {day} p.1 ---")
    exp1 = 137896
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {day} p.2 ---")
    exp2 = 501
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
