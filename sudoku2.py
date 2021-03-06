import sys
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


def resolve(n, matrix, ind, work):
    ret = []

    pos = [0 for _ in work];

    i = ind
    while i < len(work):
        while pos[i] < len(work[i][1]):
            if check(work[i][1][pos[i]], work[i][0][0], work[i][0][1], n, matrix):
                matrix[work[i][0][0]][work[i][0][1]] = work[i][1][pos[i]]
                i += 1
                break
            else:
                pos[i] += 1
        else:
            pos[i] = 0
            i -= 1
            if i < 0:
                break
            pos[i] += 1
            matrix[work[i][0][0]][work[i][0][1]] = 0
    else:
        for p in work:
            ret.append([[p[0][0], p[0][1]], matrix[p[0][0]][p[0][1]]])

    return ret


if __name__ == "__main__":
    n, matrix = read(sys.argv[1])
    if n == 0:
        exit(-1)

    print(n, matrix)

    work = []
    for i in (range(len(matrix))):
        for j in (range(len(matrix))):
            if matrix[i][j] == 0:
                l = []
                for k in (range(1, len(matrix) + 1)):
                    if check(k, i, j, n, matrix):
                        l.append(k)
                if len(l):
                    work.append([[i, j], l])

    print(work)

    t1 = time.time()
    solution = resolve(n, matrix, 0, work)
    t2 = time.time()

    print(t2 - t1)

    print(solution)

    for s in solution:
        matrix[s[0][0]][s[0][1]] = s[1]

    print(matrix)
