#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List, Tuple, Optional

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils


DEBUG = False
T_COORD = Tuple[int, int]


class Point(object):

    CARDINAL_POINTS = ('N', 'E', 'S', 'W')

    def __init__(self, xy=(0, 0)):
        self.x = xy[0]
        self.y = xy[1]
        self.direction = 'N'  # TODO: does not make sense for a Point

    def __repr__(self):
        return "<{}: {}, {}>".format(self.__class__.__name__,
            (self.x, self.y),
            self.direction)

    def turn(self, instr: str) -> str:
        '''Turn according to the instruction:
          * L -- turn 90 degrees counterclockwise
          * R -- turn 90 degrees clockwise
        Turning means changing the orientation (direction) of the Point.
        '''
        assert instr in ('L', 'R'), f"Wrong value: {instr}"
        directions = self.CARDINAL_POINTS
        if instr == 'L':
            directions = list(reversed(directions))
        idx = directions.index(self.direction)
        idx = (idx + 1) % len(self.CARDINAL_POINTS)
        self.direction = directions[idx]
        return self.direction

    def forward(self, nsteps: int) -> T_COORD:
        '''Move the Point forward given number of steps <nsteps> in the current
        direction'''
        if self.direction in ('S', 'W'):
            nsteps *= -1
        if self.direction in ('N', 'S'):
            self.y += nsteps
        elif self.direction in ('E', 'W'):
            self.x += nsteps
        return self.xy

    def move(self, instruction: str) -> T_COORD:
        '''Update the coordinates and direction of the current Point according
        to the given instruction. Instructions have the form:
         * R20 -- turn right and advance 20 units
         * L5 -- turn left and advance 5 units
        '''
        self.turn(instruction[0])
        self.forward(int(instruction[1:]))
        return self.xy

    @property
    def xy(self) -> T_COORD:
        return (self.x, self.y)


class Line(object):
    '''A Line is described by two Points: start and end'''

    def __init__(self, stp=None, endp=None):
        self.start = stp
        self.end = endp

    def intersection_point(self, other: 'Line') -> Optional[Point]:
        '''If the current line and another line <other> intersect, return
        the point where the intersection occurs. Otherwise return None'''
        if DEBUG:
            print(f"Intersecting:\n {self} vs\n {other}")
        xs = set(self.xrange()).intersection(other.xrange())
        ys = set(self.yrange()).intersection(other.yrange())
        if DEBUG:
            print(xs, ys)
        if xs and ys:
            return Point((list(xs)[0], list(ys)[0]))
        return None

    def xrange(self) -> range:
        step = 1 if self.start.x <= self.end.x else -1
        return range(self.start.x, self.end.x+step, step)

    def yrange(self) -> range:
        step = 1 if self.start.y <= self.end.y else -1
        return range(self.start.y, self.end.y+step, step)

    def __repr__(self):
        return "<{}: start={}, end={}>".format(
            self.__class__.__name__, self.start, self.end)


def solve_p1(line: str) -> int:
    """Solution to the 1st part of the challenge"""
    steps = line.strip().split(', ')
    pt = Point()
    for st in steps:
        pt.move(st)
    return abs(pt.x) + abs(pt.y)


def solve_p2(line: str) -> int:
    """Solution to the 2nd part of the challenge"""
    lines = []
    steps = line.strip().split(', ')
    head = Point()
    for st in steps:
        line = Line(Point(head.xy))
        head.move(st)
        line.end = Point(head.xy)
        if DEBUG:
            print(st, head, line)
            print("--- Finding interesections ---")
        # iterate over previously added lines and find out whether the current
        # line intersects with any of them. Not computing intersection with
        # the most recently added line because the current line obviously
        # intersects with it in the start point.
        for i in range(len(lines)-1):
            pt = line.intersection_point(lines[i])
            if pt:
                return abs(pt.x) + abs(pt.y)
        if DEBUG:
            print("--- /END ---")
        lines.append(line)
    return None


tests = [
    ("R2, L3", 5, None),
    ("R2, R2, R2", 2, None),
    ("R5, L5, R5, R3", 12, None),
    ("R8, R4, R4, R8", None, 4)
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
    day = '01'
    lines = utils.load_input()

    print(f"--- Day {day} p.1 ---")
    exp1 = 307
    res1 = solve_p1(lines[0])
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {day} p.2 ---")
    exp2 = 165
    res2 = solve_p2(lines[0])
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
