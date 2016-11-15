import sys
from collections import defaultdict


def read(fname):
    matrix = []
    n = 1

    try:
        f = open(fname, "rt")
        for str in f:
            matrix.append([int(x) for x in str.split()])
        f.close()
    except IOError:
        return 0, []

    for i in range(len(matrix)):
        if len(matrix[i]) != len(matrix):
            return 0, []

    while True:
        if n * n == len(matrix):
            return n, matrix
        elif n * n > len(matrix):
            return 0, []
        else:
            n += 1

    return 0, []


def exclude_choice(choice, choices, constraints, active_constraints):
    for constraint_to_remove in choices[choice]:
        active_constraints.remove(constraint_to_remove)
        for choice_to_remove in constraints[constraint_to_remove]:
            for constraint in choices[choice_to_remove]:
                if constraint != constraint_to_remove:
                    constraints[constraint].remove(choice_to_remove)


def include_choice(choice, choices, constraints, active_constraints):
    for constraint_to_add in choices[choice]:
        active_constraints.add(constraint_to_add)
        for choice_to_add in constraints[constraint_to_add]:
            for constraint in choices[choice_to_add]:
                if constraint != constraint_to_add:
                    constraints[constraint].add(choice_to_add)


def resolve(N, choices, constraints, active_constraints):
    if not active_constraints:
        return []

    ind = min(active_constraints, key=lambda j: len(constraints[j]))

    ret = []

    possible_choices = list(constraints[ind])
    for choice in possible_choices:
        exclude_choice(choice, choices, constraints, active_constraints)
        if not active_constraints:
            ret.append([choice])
        else:
            ret_next = resolve(N, choices, constraints, active_constraints)
            for p in ret_next:
                ret.append([choice] + p)
        include_choice(choice, choices, constraints, active_constraints)

    return ret


if __name__ == "__main__":
    n, matrix = read(sys.argv[1])
    if n == 0:
        exit(-1)

    print(n, matrix)

    N = n * n

    '''
        Row-Column constraint number is r * N + c
        Row-Number constraint number is r * N + d + N * N
        Column-Number constraint number is c * N + d + 2 * N * N
        Block-Number constraint number is b * N + d + 3 * N * N
        Block number is (r // n) * n + c // n
    '''

    choices = {i: [] for i in range(N * N * N)}
    for r in range(N):
        for c in range(N):
            for d in range(N):
                num = (r * N + c) * N + d
                choices[num].append((r * N + c) * 4)
                choices[num].append((r * N + d) * 4 + 1)
                choices[num].append((c * N + d) * 4 + 2)
                b = (r // n) + (c // n) * n
                choices[num].append((b * N + d) * 4 + 3)

    constraints = defaultdict(set)
    for i in choices:
        for j in choices[i]:
            constraints[j].add(i)

    active_constraints = set(constraints)

    initial = []
    for i in (range(N)):
        for j in (range(N)):
            if matrix[i][j] > 0:
                initial.append((i * N + j) * N + matrix[i][j] - 1)

    print(choices)
    print(constraints)
    print(active_constraints)
    print(initial)

    for i in initial:
        exclude_choice(i, choices, constraints, active_constraints)

    ret = resolve(N, choices, constraints, active_constraints)

    print(len(ret))

    if len(ret) == 1:
        res = ret[0]
        res += initial;
        for i in res:
            t, d = divmod(i, N)
            d += 1
            i, j = divmod(t, N)
            matrix[i][j] = d

        print(matrix)
