import sys
from collections import defaultdict
import multiprocessing
import copy
import time


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


def check_row(elem, i, matrix):
    for j in (range(len(matrix))):
        if matrix[i][j] == elem:
            return False
    else:
        return True


def check_column(elem, j, matrix):
    for i in (range(len(matrix))):
        if matrix[i][j] == elem:
            return False
    else:
        return True


def check_square(elem, i, j, n, matrix):
    ind1 = int(i / n)
    ind2 = int(j / n)
    for i1 in (range(ind1 * n, (ind1 + 1) * n)):
        for j1 in (range(ind2 * n, (ind2 + 1) * n)):
            if matrix[i1][j1] == elem:
                return False
    else:
        return True


def check(elem, i, j, n, matrix):
    if check_row(elem, i, matrix) \
            and check_column(elem, j, matrix) \
            and check_square(elem, i, j, n, matrix):
        return True
    else:
        return False


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
                choices[num].append(r * N + c)
                choices[num].append(r * N + d + N * N)
                choices[num].append(c * N + d + 2 * N * N)
                b = (r // n) * n + c // n
                choices[num].append(b * N + d + 3 * N * N)

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

    branch = []
    for i in (range(N)):
        for j in (range(N)):
            if matrix[i][j] == 0:
                for k in (range(1, N + 1)):
                    if check(k, i, j, n, matrix):
                        branch.append((i * N + j) * N + k - 1)
            if (len(branch)) > 0:
                break
        if (len(branch) > 0):
            break

    args = []
    arg_choices = []
    arg_constraints = []
    arg_active_constraints = []
    for b in branch:
        arg_choices.append(copy.deepcopy(choices))
        arg_constraints.append(copy.deepcopy(constraints))
        arg_active_constraints.append(copy.deepcopy(active_constraints))
        exclude_choice(b, arg_choices[len(arg_choices) - 1], arg_constraints[len(arg_constraints) - 1]
                       , arg_active_constraints[len(arg_active_constraints) - 1])
        args.append((N, arg_choices[len(arg_choices) - 1], arg_constraints[len(arg_constraints) - 1]
                     , arg_active_constraints[len(arg_active_constraints) - 1]))

    pool = multiprocessing.Pool()

    t1 = time.time()
    solutions = pool.starmap(resolve, args)
    t2 = time.time()

    print(t2 - t1)

    print([len(s) for s in solutions if len(s) > 0])
