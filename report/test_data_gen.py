from sys import stdin
import numpy as np


def print_test(id, n, f, searches):
    times = []
    gend = []
    expd = []
    for s in searches:
        times.append(str(int(np.round(float(s[0]) * 1000))))
        gend.append(str(s[1]))
        expd.append(str(s[2]))
    searches_str = (" & ").join([" & ".join(times), " & ".join(gend), " & ".join(expd)])
    print((" & ").join([id, str(n), str(f), searches_str]) + " \\\\")


stdin.readline()  # header

while first := stdin.readline():
    bfs = first.split(",")
    dfs = stdin.readline().split(",")
    greedy = stdin.readline().split(",")
    astar = stdin.readline().split(",")
    searches = [s[2:] for s in (bfs, dfs, greedy, astar)]
    name = bfs[0]

    size = 0
    free = 0

    with open("../proj-ist-unit-tests/ia/2021-2022/custom-tests/" + name) as f:  # open("tests/" + name) as f:
        lines = f.readlines()[1:]
        size = len(lines)
        free = sum([l.count("2") for l in lines])

    print_test("T" + name[len("size") : -3].replace("_", "\\_"), size, free, searches)
