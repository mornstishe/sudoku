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
    for elem in work[ind][1]:
        i, j = work[ind][0][0], work[ind][0][1]
        if check(elem, i, j, n, matrix):
            matrix[i][j] = elem
            if ind == len(work) - 1:
                ret.append([[[i, j], elem]])
            else:
                ret_next = resolve(n, matrix, ind + 1, work)
                for p in ret_next:
                    ret.append([[[i, j], elem]] + p)
            matrix[i][j] = 0

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

    print(len(solution))

    if (len(solution) == 1):
        for s in solution[0]:
            matrix[s[0][0]][s[0][1]] = s[1]

        print(matrix)
