#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List
import hashlib

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils


DEBUG = False


def solve_p1(line: str) -> int:
    """Solution to the 1st part of the challenge"""
    password = ''
    idx = -1
    while len(password) < 8:
        idx += 1
        m = hashlib.md5()
        m.update(bytes(line + str(idx), 'utf8'))
        hexdig = m.hexdigest()
        if hexdig.startswith('00000'):
            password += hexdig[5]
            if DEBUG:
                print(f"Password: {password} from {hexdig}")
    return password


def solve_p2(line: str) -> int:
    """Solution to the 2nd part of the challenge"""
    password = [None] * 8
    idx = -1
    while password.count(None):
        idx += 1
        m = hashlib.md5()
        m.update(bytes(line + str(idx), 'utf8'))
        hexdig = m.hexdigest()
        if hexdig.startswith('00000'):
            pos, char = hexdig[5:7]
            if pos in '01234567' and password[int(pos)] is None:
                password[int(pos)] = char
                if DEBUG:
                    print(f"Password: {password} from {hexdig}")
    return "".join(password)


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
