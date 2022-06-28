from sys import stdin

# Input: compare_searchers output, collected with searchers.sh, modified with:
# for s in searchers:
#     p = do(s, problems[0])
#     print(str(name(s)) + "," + str(p.succs) + "," + str(p.states))
# return

# [worse, same, better]
greedy_score_gen = [0, 0, 0]
greedy_score_exp = [0, 0, 0]

while test := stdin.readline():
    dfs = stdin.readline()
    (dfs_gen, dfs_exp) = map(int, dfs.split(",")[1:])
    greedy = stdin.readline()
    (greedy_gen, greedy_exp) = map(int, greedy.split(",")[1:])

    if dfs_gen < greedy_gen:
        greedy_score_gen[0] += 1
    elif dfs_gen == greedy_gen:
        greedy_score_gen[1] += 1
    else:
        greedy_score_gen[2] += 1

    if dfs_exp < greedy_exp:
        greedy_score_exp[0] += 1
    elif dfs_exp == greedy_exp:
        greedy_score_exp[1] += 1
    else:
        greedy_score_exp[2] += 1

print("type: [ worse, same, better ] : score")
print("gen:", greedy_score_gen, ":", greedy_score_gen[2] - greedy_score_gen[0])
print("exp:", greedy_score_exp, ":", greedy_score_exp[2] - greedy_score_exp[0])
print("Overall score:", greedy_score_gen[2] - greedy_score_gen[0] + greedy_score_exp[2] - greedy_score_exp[0])
