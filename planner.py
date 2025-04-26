#!/usr/bin/env python3
import sys, heapq

class N:
    def __init__(self, st, p=None, a=None, c=0):
        self.st, self.p, self.a, self.c = st, p, a, c

def load(f):
    l = [x.rstrip() for x in open(f) if x.strip()]
    c, r = int(l[0]), int(l[1])
    g = l[2:]
    s = None
    d = set()
    b = set()
    for i, row in enumerate(g):
        for j, ch in enumerate(row):
            if ch == '@': s = (i, j)
            elif ch == '*': d.add((i, j))
            elif ch == '#': b.add((i, j))
    return r, c, s, frozenset(d), b

def succ(st, r, c, b):
    (i, j), d = st
    res = []
    if (i, j) in d:
        nd = set(d)
        nd.remove((i, j))
        res.append(('V', ((i, j), frozenset(nd))))
    for m, (di, dj) in [('N',(-1,0)),('S',(1,0)),('W',(0,-1)),('E',(0,1))]:
        ni, nj = i+di, j+dj
        if 0 <= ni < r and 0 <= nj < c and (ni, nj) not in b:
            res.append((m, ((ni, nj), d)))
    return res

def dfs(st, r, c, b):
    gen = 1
    exp = 0
    fr = [N(st)]
    vis = {st}
    while fr:
        n = fr.pop()
        exp += 1
        pos, d = n.st
        if not d:
            return n, gen, exp
        for a, nst in succ(n.st, r, c, b):
            if nst not in vis:
                vis.add(nst)
                fr.append(N(nst, n, a))
                gen += 1
    return None, gen, exp

def ucs(st, r, c, b):
    gen = 1
    exp = 0
    cnt = 0
    pq = [(0, cnt, N(st))]
    best = {st: 0}
    while pq:
        cost, _, n = heapq.heappop(pq)
        exp += 1
        pos, d = n.st
        if not d:
            return n, gen, exp
        for a, nst in succ(n.st, r, c, b):
            nc = cost + 1
            if nst not in best or nc < best[nst]:
                best[nst] = nc
                cnt += 1
                heapq.heappush(pq, (nc, cnt, N(nst, n, a, nc)))
                gen += 1
    return None, gen, exp

def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: python3 planner.py [depth-first|uniform-cost] file")
    alg, fn = sys.argv[1], sys.argv[2]
    r, c, s, d, b = load(fn)
    start = (s, d)
    if alg == "depth-first":
        goal, gen, exp = dfs(start, r, c, b)
    elif alg == "uniform-cost":
        goal, gen, exp = ucs(start, r, c, b)
    else:
        sys.exit("Use depth-first or uniform-cost")
    if not goal:
        sys.exit("No sol")
    acts = []
    n = goal
    while n.p:
        acts.append(n.a)
        n = n.p
    for mv in reversed(acts):
        print(mv)
    print(f"{gen} nodes generated")
    print(f"{exp} nodes expanded")

if __name__ == "__main__":
    main()