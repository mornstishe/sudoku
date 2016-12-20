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
    if matrix[i].count(elem):
        return False
    else:
        return True


def check_column(elem, j, matrix):
    if matrix[j].count(elem):
        return False
    else:
        return True


def check_square(elem, i, j, n, matrix):
    if matrix[(i // n) * n + j // n].count(elem):
        return False
    else:
        return True


def check(elem, i, j, n, matrix, matrix2, matrix3):
    if check_row(elem, i, matrix) \
            and check_column(elem, j, matrix2) \
            and check_square(elem, i, j, n, matrix3):
        return True
    else:
        return False


def resolve(n, matrix, ind, work, matrix2, matrix3):
    ret = []
    for elem in work[ind][1]:
        i, j = work[ind][0][0], work[ind][0][1]
        if check(elem, i, j, n, matrix, matrix2, matrix3):
            matrix[i][j] = elem
            matrix2[j][i] = elem
            matrix3[(i // n) * n + j // n][(i % n) * n + j % n] = elem
            if ind == len(work) - 1:
                ret.append([[[i, j], elem]])
            else:
                ret_next = resolve(n, matrix, ind + 1, work, matrix2, matrix3)
                for p in ret_next:
                    ret.append([[[i, j], elem]] + p)
            matrix[i][j] = 0
            matrix2[j][i] = 0
            matrix3[(i // n) * n + j // n][(i % n) * n + j % n] = 0

    return ret


if __name__ == "__main__":
    n, matrix = read(sys.argv[1])
    if n == 0:
        exit(-1)

    print(n, matrix)
    matrix2 = [[matrix[j][i] for j in range(n * n)] for i in range(n * n)]
    matrix3 = [[matrix[(i // n) * n + j // n][(i % n) * n + j % n] for j in range(n * n)] for i in range(n * n)]
    work = []
    for i in (range(len(matrix))):
        for j in (range(len(matrix))):
            if matrix[i][j] == 0:
                l = []
                for k in (range(1, len(matrix) + 1)):
                    if check(k, i, j, n, matrix, matrix2, matrix3):
                        l.append(k)
                if len(l):
                    work.append([[i, j], l])

    print(work)

    while True:
        wc1 = len(work)
        chk = False
        for ind in range(len(work)):
            if len(work[ind][1]) == 1:
                i, j = work[ind][0][0], work[ind][0][1]
                matrix[i][j] = work[ind][1][0]
                matrix2[j][i] = work[ind][1][0]
                matrix3[(i // n) * n + j // n][(i % n) * n + j % n] = work[ind][1][0]
                chk = True
        if chk:
            ind = 0
            while ind < len(work):
                for k in (work[ind][1]):
                    i, j = work[ind][0][0], work[ind][0][1]
                    if not check(k, i, j, n, matrix, matrix2, matrix3):
                        work[ind][1].remove(k)
                if len(work[ind][1]) == 0:
                    del work[ind]
                else:
                    ind += 1
        wc2 = len(work)
        if wc1 == wc2:
            break

    t1 = time.time()
    if len(work):
        solution = resolve(n, matrix, 0, work, matrix2, matrix3)
    else:
        solution = []
    t2 = time.time()

    print(t2 - t1)

    print(len(solution))

    if len(solution) == 1:
        for s in solution[0]:
            matrix[s[0][0]][s[0][1]] = s[1]

        print(matrix)

    if (len(work) == 0):
        print(matrix)
