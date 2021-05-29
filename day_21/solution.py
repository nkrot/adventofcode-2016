#!/usr/bin/env python

# # #
# TODO
# why does test 2.0 fail? is scrambling process reversible?

import re
import os
import sys
from typing import List

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils

DAY = '21'
DEBUG = False


def parse_commands(lines: List[str]) -> List[tuple]:
    cmds = []
    for line in lines:
        tokens = line.strip().split()
        if tokens:
            # print(tokens)
            cmd, args = [tokens[0]], []
            if tokens[0] in {'swap', 'move'} and tokens[1] == 'position':
                args = (int(tokens[2]), int(tokens[5]))
            elif tokens[0] == 'swap':
                args = (tokens[2], tokens[5])
            elif tokens[0] == 'reverse':
                args = (int(tokens[2]), int(tokens[4]))
            elif tokens[0] == 'rotate' and tokens[1] in {'left', 'right'}:
                sign = -1 if tokens[1] == 'left' else 1
                args = (sign * int(tokens[2]), )
            elif tokens[0] == 'rotate' and tokens[5] == 'letter':
                args = (tokens[6], )
            else:
                raise ValueError(f"Cannot parse: '{line}'")

            cmd.extend(args)
            # print(cmd)
            cmds.append(tuple(cmd))
    return cmds


def lrotate(items: list, nsteps: int) -> list:
    '''Rotate given list <nsteps> to the right is nsteps is positive or
    to the left if nsteps is negative'''
    i = nsteps * -1
    if abs(i) > len(items):
        i = i % len(items) * (i // abs(i))
    head, tail = items[:i], items[i:]
    return tail + head


def scramble(inp: str, rules: List[tuple], undo=False) -> str:
    chars = list(inp)
    if undo:
        rules = reversed(rules)

    for r in rules:
        if DEBUG:
            print(r)
            print(f"< {chars}")

        if r[0] == 'swap' and isinstance(r[1], int):
            i, j = r[1:]
            chars[i], chars[j] = chars[j], chars[i]

        elif r[0] == 'swap' and isinstance(r[1], str):
            # TODO: what if occur more than once?
            # TODO: what if occur different number of times, say, 1 and 2
            i, j = r[1:]
            i, j = chars.index(i), chars.index(j)
            chars[i], chars[j] = chars[j], chars[i]

        elif r[0] == 'reverse':
            i, j = r[1:]
            chars = chars[:i] + list(reversed(chars[i:j+1])) + chars[j+1:]

        elif r[0] == 'rotate' and isinstance(r[1], int):
            i = r[1]
            if undo:
                i *= -1
            chars = lrotate(chars, i)

        elif False and r[0] == 'rotate' and isinstance(r[1], str):
            i = chars.index(r[1])
            if i > 3:
                i += 1
            i = i+1
            if i > len(chars):
                i = i % len(chars)
            chars = lrotate(chars, i)

        elif r[0] == 'rotate' and isinstance(r[1], str):
            rotations = build_rotation_map(chars)
            s = chars.index(r[1])
            if undo:
                for rot in rotations:
                    if rot[1] == s:
                        break
                nsteps = rot[0] * -1
            else:
                nsteps = rotations[s][0]
            chars = lrotate(chars, nsteps)

        elif r[0] == 'move' and isinstance(r[1], int):
            i, j = r[1:]
            if undo:
                i, j = j, i
            char = chars.pop(i)
            chars.insert(j, char)

        else:
            raise ValueError(f'Cannot handle command: {r}')

        if DEBUG:
            print(f"> {chars}")

    return ''.join(chars)


def build_rotation_map(chars: List[str]):
    '''For each (start) position in the list <chars> compute
    * its rotation <nsteps> and
    * its end position, into which the items at start position will go once
      the rotation by nsteps was applied.'''
    positions = []
    for spos in range(len(chars)):
        epos = spos
        nsteps = 1 + spos
        if spos > 3:
            nsteps += 1
        if nsteps >= len(chars):
            nsteps %= len(chars)
        # what will i be after rotation?
        epos += nsteps
        if epos >= len(chars):
            epos %= len(chars)
        positions.append((nsteps, epos))
    return positions


def test_rotation_maps():
    chars = list('abcdef')
    print(f"< {chars}")
    positions = build_rotation_map(chars)
    print(positions)
    for spos, rot in enumerate(positions):
        nsteps, epos = rot
        res = lrotate(chars, nsteps)
        print(spos, chars[spos], rot, res, res[epos], chars[spos] == res[epos])

# test_rotation_maps()
# exit(100)


def solve_p1(lines: List[str], password: str) -> str:
    """Solution to the 1st part of the challenge"""
    commands = parse_commands(lines)
    res = scramble(password, commands)
    return res


def solve_p2(lines: List[str], scrambled: str) -> int:
    """Solution to the 2nd part of the challenge"""
    commands = parse_commands(lines)
    return scramble(scrambled, commands, True)


text_1 = """\
swap position 4 with position 0
swap letter d with letter b
reverse positions 0 through 4
rotate left 1 step
move position 1 to position 4
move position 3 to position 0
rotate based on position of letter b
rotate based on position of letter d
"""


tests = [
    (text_1.split('\n'), 'decab', 'abcde'),
]


def run_tests():
    print("--- Tests ---")

    for tid, (inp, exp1, exp2) in enumerate(tests):
        if exp1 is not None:
            res1 = solve_p1(inp, exp2)
            print(f"T1.{tid}:", res1 == exp1, exp1, res1)

        if exp2 is not None:
            res2 = solve_p2(inp, exp1)
            print(f"T2.{tid}:", res2 == exp2, exp2, res2)


def run_real():
    lines = utils.load_input()

    print(f"--- Day {DAY} p.1 ---")
    exp1 = 'agcebfdh'
    res1 = solve_p1(lines, 'abcdefgh')
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {DAY} p.2 ---")
    exp2 = 'afhdbegc'
    res2 = solve_p2(lines, 'fbgdceah')
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
