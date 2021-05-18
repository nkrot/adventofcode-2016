#!/usr/bin/env python

# # #
#
#

import re
import os
import sys
from typing import List, Tuple, Callable
from hashlib import md5
from collections import defaultdict

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from aoc import utils


DEBUG = False


def parse(hcode: str) -> Tuple[str, List[str]]:
    hcode = hcode + ",,"
    st = 0
    # print(hcode)
    sub3s, sub5s = [], set()
    while st < len(hcode)-4:
        sub5 = hcode[st:st+5]
        sub3 = hcode[st:st+3]
        incr = 1
        if not sub3s and sub3 == ''.join(sub3[0] * 3):
            # print("... take 3")
            sub3s.append(sub3)
            incr = 3
        if sub5 == ''.join(sub5[0] * 5):
            # print("... take 5")
            sub5s.add(sub5)
            incr = 5
        st += incr
    return sub3s, sub5s


# solve1:
# real 56,33; user 56,06
# Conclusion: Surprise! solve2 is no better than solve1. Disappointed.

# solve2:
# 1) [confirmed1] real 55,19; user 54,71
# 2) [confirmed2] real 53,66; user 53,34
# 3) [confirmed2] real 56,44; user 56,20
# Conclusion: Surprise. There is not benefit in using dict-based approach
# to checking key validity over list-based, probably because the cost of
# maintaining the dict-based structure is still high.

# for larger input: 64*2 keys are generated
# 4) [confirmed1] real 120,66; user 119,89
# 5) [confirmed2] real 121,26; user 120,59


def solve2(hasher: Callable) -> int:
    '''
    This algorithm addresses problems described in solve1():
    - it searches (forward) for Qx when looking at a Tx
    '''
    keys = []
    DISTANCE = 1000

    hashes = [None] * DISTANCE
    confirms = defaultdict(set)  # for confirmed2()

    def set_hash(pos: int):
        addr = pos % DISTANCE
        hcode = hasher(pos)
        hashes[addr] = (pos, hcode)
        if False:  # enable it for confirmed2()
            for ch in re.findall(r'(.)\1\1\1\1', hcode):
                key = ch*3
                confirms[key].add(pos)
        return hcode

    def get_hash(pos: int):
        return hashes[pos % DISTANCE][-1]

    def confirmed1(key: str, pos: int):
        target = key[0] * 5
        for i in range(1+pos, 1+pos+DISTANCE):
            if target in get_hash(i):
                return True
        return False

    def confirmed2(key: str, kpos: int):
        positions = confirms.get(key, [])
        obsoletes = [qpos for qpos in positions if kpos >= qpos]
        if obsoletes:
            positions.difference_update(obsoletes)
        return bool(positions)

    # create future hash sums
    for i in range(0, DISTANCE):
        set_hash(i)

    i = -1
    while len(keys) <= 64:
        i += 1
        hsh = get_hash(i)
        set_hash(i+DISTANCE)  # create future hash sum
        m = re.search(r'(.)\1\1', hsh)
        if m and confirmed1(m[0], i):
            keys.append((i, m[0]))

    # print(keys)
    return keys[63][0]


def solve1(hasher: Callable) -> int:
    '''
    The algorithm stores candidate keys (triples) and confirms some of them
    when inspecting the current quantuple by checking candidate keys collected
    from immediately preceeding positions.

    Problems (encountered when doing part 2)
    1) (real) a candidate key can be confirmed more than once, leading to
       appearance of duplicates in the list of keys:
       .. T1 .. ..  Q1 .. .. Q1
       => this is solved by deduplicating the list of keys

    2) (potential) a good key seen early can be missed because later keys fill
       up the necessary quantity (64) and further search is not performed.
       .. T1 .. .. T2 .. T3 .. Q2 .. Q3 .. Q1 ..
       In the example, the key T1 can be missed when Q3 is reached that
       confirms the key T3 and the number of keys found so far becomes 64.
       In the current algorithm, the search stop at this point.
       => the search should continue as long as ...
          The search algorithm is too complex :)
          TODO: Do something else, for example, search for Q1 when looking at
          the candidate key T1. This will guarantee that T1 is found.
    '''

    keys = set()
    memory = defaultdict(list)

    def store_key(triples: list, pos: int):
        if triples:
            memory[triples[0]].append(pos)

    def find_key(qtuples: list, pos: int):
        '''
        TODO: a confirmed key should be removed from the memory. Thus duplicate
        key will not be added. Note that <qtuples> should be uniqued, otherwise
        the same key can be confirmed more than once (duplicated) inside this
        very function.

        TODO: memory stores keys that are outside of the reach. This could be
        an issue for larger problems.
        '''
        keys = []
        for item in qtuples:
            triple = item[0:3]
            positions = memory.get(triple, [])
            for idx, key_pos in enumerate(positions):
                if pos - key_pos <= 1000:
                    keys.append((triple, key_pos))
                    # positions.remove(key_pos)  # wrong
                    # break # wrong
        return keys

    i = -1
    while len(keys) <= 64:
        i += 1

        hsh = hasher(i)
        triples, quintuples = parse(hsh)

        # if triples:
        #     print(i, hsh)
        #     print(triples, quintuples)

        candidate_keys = find_key(quintuples, i)
        if candidate_keys:
            # print(f"... found key: {candidate_keys}")
            keys.update(candidate_keys)

        store_key(triples, i)

    keys = sorted(keys, key=lambda vs: vs[-1])
    if DEBUG:
        print(i, len(keys), keys)

    return keys[63][-1]


def solve_p1(salt: int) -> int:
    """Solution to the 1st part of the challenge"""
    def hasher(i):
        return md5(f"{salt}{i}".lower().encode()).hexdigest()
    # return solve1(hasher)
    return solve2(hasher)


def solve_p2(salt: int) -> int:
    """Solution to the 2nd part of the challenge"""
    def hasher(i):
        x = f'{salt}{i}'
        for _ in range(0, 2017):
            x = md5(x.lower().encode()).hexdigest()
        return x
    # return solve1(hasher)
    return solve2(hasher)


tests = [
    # ('abc', 22728, None),
    ('abc', 22728, 22551),
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
    day = '14'
    inp = 'cuanljph'

    print(f"--- Day {day} p.1 ---")
    exp1 = 23769
    res1 = solve_p1(inp)
    print(exp1 == res1, exp1, res1)

    print(f"--- Day {day} p.2 ---")
    exp2 = 20606
    res2 = solve_p2(inp)
    print(exp2 == res2, exp2, res2)


if __name__ == '__main__':
    run_tests()
    run_real()
