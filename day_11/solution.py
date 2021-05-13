#!/usr/bin/env python

# # #
# TODO
# 1. Rank intermediate scenes by their "goodness" so that better ones are
#    explored earlier that others. A* algorithm?
#
# Heuristics to check
# 1) when there are compatible xM and xG on a floor, always move them up
#    together? Never consider moving them separately.
# 2) there is no need to bring *two* devices downstairs.


import re
import os
import sys
from copy import deepcopy
from typing import List, Generator
from itertools import combinations

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils


DEBUG = False
VERBOSE = False


class ElevatorError(Exception):
    pass


class Scene(object):

    VOCABULARY = {
        'cobalt'     : 'Co',
        'hydrogen'   : 'H',
        'lithium'    : 'Li',
        'polonium'   : 'Po',
        'promethium' : 'Pm',
        'ruthenium'  : 'Ru',
        'thulium'    : 'Tm',
        'elerium'    : 'Lr',
        'dilithium'  : 'Dl',
        'microchip'  : 'M',
        'generator'  : 'G',
        # 'elevator'   : 'E'
    }

    count = 0

    @classmethod
    def from_lines(cls, lines: List[str]) -> 'Scene':
        obj = cls()
        obj.elevator_at = 0
        reg = re.compile(r'(\S+?)(:?-compatible)? (generator|microchip)')
        for line in lines:
            floor = []
            for m in re.finditer(reg, line):
                device = "{}{}".format(cls.VOCABULARY[m.group(1)],
                                       cls.VOCABULARY[m.group(3)])
                floor.append(device)
            obj.floors.append(floor)
        return obj

    def __init__(self, other = None):
        self.floors = []
        self._devices = None
        self.elevator_at = 0
        self.time = 0
        self.origin = None

        if other is not None:
            subdict = {k: v for k, v in other.__dict__.items()
                            if k not in {'origin'}}
            self.__dict__ = deepcopy(subdict)
            self.origin = other

        self.__class__.count += 1

    @property
    def devices(self) -> List[str]:
        '''A sorted list of all devices (codes) available on the scene.
        This method should be called only when the full schene is available,
        otherwise the list of devices will be incomplete.'''
        if not self._devices:
            devs = set()
            for objects in self.floors:
                devs.update(objects)
            self._devices = sorted(devs)
        return self._devices

    def __str__(self) -> str:
        lines = []
        for idx, objects in enumerate(self.floors):
            tokens = [f"F{1+idx}", "."] + ['.'] * len(self.devices)
            if self.elevator_at == idx:
                tokens[1] = 'E'
            for obj in objects:
                tokens[2+self.devices.index(obj)] = obj
            lines.append(''.join(f'{t:4}' for t in tokens))
        return "\n".join(reversed(lines))

    @property
    def elevator_cargo(self) -> List[str]:
        '''Return list of objects that are in the elevator'''
        return list(self.floors[self.elevator_at])

    def go_up(self, *objects):
        '''Move <objects> one floor up'''
        # print(f"Elevator[{self.elevator_at}] moves up {objects}")
        if self.elevator_at >= self.last_floor_id:
            raise ElevatorError("Elevator cannot go above the highest floor")
        self._goto(self.elevator_at+1, *objects)
        return self

    def go_down(self, *objects):
        '''Move <objects> one floor down'''
        # print(f"Elevator[{self.elevator_at}] moves down {objects}")
        if self.elevator_at <= 0:
            raise ElevatorError("Elevator cannot go below the lowest floor")
        self._goto(self.elevator_at-1, *objects)
        return self

    def _goto(self, floor, *objects):
        '''Move given objects from the current floor to the given floor'''
        if not objects:
            raise ElevatorError("Empty elevator can not move.")
        for obj in objects:
            try:
                self.floors[self.elevator_at].remove(obj)
            except ValueError:
                raise ElevatorError(f"Object not in the elevator: {obj}")
            self.floors[floor].append(obj)
        self.elevator_at = floor
        self.time += 1

    @property
    def last_floor_id(self) -> int:
        '''Return number of the last floor in the area'''
        return len(self.floors) - 1

    def __hash__(self):
        '''Makes the object hashable and therefore usable as keys in
        a dictionary and also comparable by equality.
        For the task at hand, only a subset of fields determines equality:
          * position of the elevator
          * objects on each floor.
        and only these fields are part of the hash sum.
        '''
        data = [self.elevator_at]
        for floor in self.floors:
            data.append(tuple(sorted(floor)))
        return hash(tuple(data))

    def __eq__(self, other: 'Scene'):
        return hash(self) == hash(other)

    def compatible(self, *objects):
        '''
        If called with one argument, return corresponding compatible device,
        that is, a generator for given microchip and a microchip for given
        generator.
        If called with two arguments, return both arguments as a tuple if
        given devices are compatible. Otherwise, return an empty tuple.

        Examples:
        compatible('LiG') --> 'LiM'
        compatible('LiG', 'LiM')) --> ('LiG', 'LiM')
        compatible('LiG', 'TmM')) --> ()
        '''
        if len(objects) == 1:
            obj = objects[0]
            obj = obj[:-1] + ('G' if obj[-1] == 'M' else 'M')
        elif len(objects) == 2:
            obj = ()
            if objects[1] == self.compatible(objects[0]):
                obj = objects
        else:
            raise ValueError("Wrong number of arguments")
        return obj

    def counts(self) -> List[int]:
        '''Return number of objects on each floor'''
        counts = [len(objects) for objects in self.floors]
        return counts


# Number of scenes explored:
# 0 | 2009 | 2_922_003 | sucks
# A | 1574 | 2_632_642 | sucks


def mutate(scene: Scene,
           memo={'go_up': set(), 'go_down': set()}
    ) -> Generator[Scene, None, None]:

    '''Generate all possible variations of the the current scene that differ
    from the current by exactly one step. One step means the elevator can move
     * one or two objects (each one and every combination of two objects),
     * one level up or down the area.
    Do not produce variations that have already been seen in the past.
    '''

    objects = scene.elevator_cargo
    subsets = []
    for num in range(1, 1+min(2, len(objects))):
        for objs in combinations(objects, num):
            subsets.append(objs)

    def reorder(devices):
        key = len(devices)
        if key == 2 and not scene.compatible(*devices):
            key += 1
        return key

    # print(f"< SUBSETS: {subsets}")
    # subsets.sort(key=reorder)
    # print(f"> SUBSETS: {subsets}")

    # moving objects up
    for objs in subsets:
        try:
            newscene = Scene(scene).go_up(*objs)
            if newscene not in memo['go_up']:
                memo['go_up'].add(newscene)
                yield newscene
        except ElevatorError:
            pass
        # if len(objs) > 1 and scene.compatible(*objs):
        #     break

    # A) Don't move objects down if all floors below are already empty.
    if sum(scene.counts()[:scene.elevator_at]) == 0:
        return

    # moving objects down
    for objs in subsets:
        try:
            newscene = Scene(scene).go_down(*objs)
            if newscene not in memo['go_down']:
                memo['go_down'].add(newscene)
                yield newscene
        except ElevatorError:
            pass



FINISHED = 0
CHIP_FRIED = -1
CHIP_SAFE = 1

LABELS = {
    FINISHED   : 'STOP, all done.',
    CHIP_FRIED : 'STOP, chip destroyed.',
    CHIP_SAFE  : 'CONTINUE, chip is safe.'
}


def evaluate(scene: Scene) -> int:
    '''Fitness function.
    Evaluate the arrangement of objects and return a status, one of:
    * FINISHED -- all objects at the last floor
    * CHIP_FRIED -- if a microchip was fried (destroyed) by a generator
    * CHIP_SAFE -- arrangement of objects is valid but not yet finished
    '''

    if sorted(scene.floors[scene.last_floor_id]) == sorted(scene.devices):
        return FINISHED

    for objects in scene.floors:
        generators = [o for o in objects if o.endswith('G')]
        if not generators:
            continue
        for chip in filter(lambda o: o.endswith('M'), objects):
            if scene.compatible(chip) not in generators:
                return CHIP_FRIED

    return CHIP_SAFE


def dprint(msg, scene=None):
    if DEBUG:
        print(msg)
        if scene:
            print(scene)


def replay(scene: Scene):
    '''Show all scenes that lead to the given one.'''
    scenes = [scene]
    while scenes[-1].origin:
        scenes.append(scenes[-1].origin)
    for idx, sc in enumerate(reversed(scenes)):
        print(f"-- scene #{idx} [time={sc.time}] --")
        print(sc)


def solve_p1(lines: List[str]) -> int:
    """Solution to the 1st part of the challenge"""
    Scene.count = 0

    scenes = [Scene.from_lines(lines)]
    best_time = 100000
    solutions = []

    # Search for solutions in BFS manner. This guarantees that better
    # solutions are discovered before worse solutions.
    while scenes:
        scene = scenes.pop(0)
        dprint(f"--- BASE SCENE [time={scene.time}] ---", scene)
        dprint("-- Generating next steps --")

        for idx, sc in enumerate(mutate(scene)):
            dprint(f"-- new scene {idx} [time={sc.time}] --", sc)
            status = evaluate(sc)
            dprint(f"--> {LABELS[status]}")
            if status == FINISHED:
                best_time = min(sc.time, best_time)
                solutions.append(sc)

                if VERBOSE:
                    print(f"--- SOLUTION #{len(solutions)} [time={sc.time}] ---")
                    replay(sc)
                    print("--- SOLUTION END ---", flush=True)

            elif status == CHIP_SAFE:
                if sc.time < best_time:
                    scenes.append(sc)
                else:
                    dprint("--> STOP, not best solution")
        dprint('')

    # for idx, solution in enumerate(solutions):
    #     print(f"--- SOLUTION #{idx} [time={solution.time}] ---")
    #     replay(solution)

    print("Number of scenes explored:", Scene.count)

    return best_time


def solve_p2(lines: List[str]) -> int:
    """Solution to the 2nd part of the challenge"""
    addons = [
        'An elerium generator.',
        'An elerium-compatible microchip.',
        'A dilithium generator.',
        'A dilithium-compatible microchip.'
    ]
    lines[0] += ' ' + ' '.join(addons)
    return solve_p1(lines)


text_1 = """\
The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant."""


tests = [
    (text_1.split('\n'), 11, None)
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
    day = '11'
    lines = utils.load_input()

    print(f"--- Day {day} p.1 ---")
    exp1 = 47
    res1 = solve_p1(lines)
    print(exp1 == res1, exp1, res1)

    # print(f"--- Day {day} p.2 ---")
    # exp2 = -1
    # res2 = solve_p2(lines)
    # print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
