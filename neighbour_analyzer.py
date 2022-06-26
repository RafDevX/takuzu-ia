# Calculates the percentage of neighbours that are of the same type
# Used for statistics for the affinity heuristic

from sys import stdin
from numpy import round


def fmt_percentage(x: float):
    return f"{str(int(round(x*100))).rjust(3)}%"


matrix = []
while row := stdin.readline():
    matrix.append(list(map(lambda x: int(x), row.split("\t"))))

affinities = []
for i in range(len(matrix)):
    for j in range(len(matrix)):
        value = matrix[i][j]
        count = 0
        total = 0

        for direction in ((0, 1), (1, 0)):
            for delta in (-1, 1):
                (row, col) = (i + direction[0] * delta, j + direction[1] * delta)
                if 0 <= row < len(matrix) and 0 <= col < len(matrix):
                    if matrix[row][col] == value:
                        count += 1
                    total += 1

        affinities.append(count / total)
        print(f"{value} ({fmt_percentage(affinities[-1])})", end="\t")
    print()

print("---- AFFINITIES ----")
print(f"Avg: {fmt_percentage(sum(affinities) / len(affinities))}")
print(f"Range: [{fmt_percentage(min(affinities))}, {fmt_percentage(max(affinities))}]")
print(f"Median: {fmt_percentage(sorted(affinities)[len(affinities) // 2])}")
