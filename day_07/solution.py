#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List
from collections import defaultdict

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils


DEBUG = False


def supports_tls(ip: str) -> bool:
    if DEBUG:
        print(ip)
    hypernet = False
    abbas = []
    for st in range(0, len(ip)-3, 1):
        substr = ip[st:st+4]
        if substr.startswith('['):
            hypernet = True
        elif substr.startswith(']'):
            hypernet = False
        if len(set(substr[0:2])) == 2 and substr[0:2] == substr[-1:-3:-1]:
            abbas.append((substr, st, not hypernet))
    if DEBUG:
        print(abbas)
    return (abbas and all(abba[-1] for abba in abbas))


def supports_ssl(ip: str) -> bool:
    if DEBUG:
        print(ip)
    hypernet = False
    sequences = defaultdict(list)
    for st in range(0, len(ip)-2, 1):
        substr = ip[st:st+3]
        if substr.startswith('['):
            hypernet = True
        elif substr.startswith(']'):
            hypernet = False
        if set(substr).intersection('[]'):
            continue
        if len(set(substr[0:2])) == 2 and substr[0] == substr[-1]:
            key = substr[1] + substr[0] + substr[1] if hypernet else substr
            sequences[key].append(hypernet)
    if DEBUG:
        print(sequences)
    for vals in sequences.values():
        if True in vals and False in vals:
            return True
    return False


def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge"""
    ips = [supports_tls(line) for line in lines]
    return ips.count(True)


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    ips = [supports_ssl(line) for line in lines]
    return ips.count(True)


text_1 = """abba[mnop]qrst
abcd[bddb]xyyx
aaaa[qwer]tyui
ioxxoj[asdfgh]zxcvbn"""


text_2 = """aba[bab]xyz
xyx[xyx]xyx
aaa[kek]eke
zazbz[bzb]cdb"""


tests = [
    (text_1.split('\n'), 2, None),
    (text_2.split('\n'), None, 3),
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
    day = '07'
    lines = utils.load_input()

    print(f"--- Day {day} p.1 ---")
    exp1 = 115
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {day} p.2 ---")
    exp2 = 231
    res2 = solve_p2(lines)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
