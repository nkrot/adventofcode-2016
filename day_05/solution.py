#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import Callable
import hashlib

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils


DEBUG = False


class Password(object):

    def __init__(self, maxlen):
        self.maxlen = maxlen
        self.chars = [None] * self.maxlen

    def __len__(self):
        return len(self.chars) - self.chars.count(None)

    def __str__(self):
        return "".join(str(ch) for ch in self.chars)

    def __add__(self, char: str):
        pos = self.chars.index(None)
        self.chars[pos] = char
        return self

    def __getitem__(self, pos: int):
        return self.chars[pos]

    def __setitem__(self, pos: int, val: str):
        self.chars[int(pos)] = val


def digests(prefix):
    '''Generate suitable MD5 digests'''
    idx = -1
    while True:
        idx += 1
        m = hashlib.md5()
        m.update(bytes(prefix + str(idx), 'utf8'))
        hexdig = m.hexdigest()
        if hexdig.startswith('00000'):
            yield(hexdig)


def solve(line: str, compose: Callable) -> str:
    '''Generic solver for both parts'''
    passwd = Password(8)
    for hexdig in digests(line):
        passwd = compose(passwd, hexdig)
        if len(passwd) >= 8:
            break
    return str(passwd)


def solve_p1(line: str) -> str:
    """Solution to the 1st part of the challenge"""

    def composer(password, digest):
        res = password + digest[5]
        if DEBUG:
            print(f"Password: {password.chars} from {digest}")
        return res

    return solve(line, composer)


def solve_p2(line: str) -> str:
    """Solution to the 2nd part of the challenge"""

    def composer(password, digest):
        pos, char = digest[5:7]
        if pos in '01234567' and password[int(pos)] is None:
            password[int(pos)] = char
            if DEBUG:
                print(f"Password: {password.chars} from {digest}")
        return password

    return solve(line, composer)


tests = [
    ('abc', '18f47a30', '05ace8e3'),
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
    day = '05'
    inp = 'ojvtpuvg'

    print(f"--- Day {day} p.1 ---")
    exp1 = '4543c154'
    res1 = solve_p1(inp)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {day} p.2 ---")
    exp2 = '1050cbbd'
    res2 = solve_p2(inp)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
