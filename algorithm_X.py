import copy

A = [['A', [1, 0, 0, 1, 0, 0, 1]] \
    , ['B', [1, 0, 0, 1, 0, 0, 0]] \
    , ['C', [0, 0, 0, 1, 1, 0, 1]] \
    , ['D', [0, 0, 1, 0, 1, 1, 0]] \
    , ['E', [0, 1, 1, 0, 0, 1, 1]] \
    , ['F', [0, 1, 0, 0, 0, 0, 1]]]


def alg(A):
    cnt = len(A) + 1
    for j in range(len(A[0][1])):
        c = 0
        for i in range(len(A)):
            c += A[i][1][j]
        if c < cnt:
            col = j
            cnt = c
    else:
        if cnt == 0:
            return []

    for i in range(len(A)):
        if A[i][1][col] == 1:
            A2 = copy.deepcopy(A)
            for j in reversed(range(len(A[i][1]))):
                if A[i][1][j] == 1:
                    for i2 in reversed(range(len(A2))):
                        if A2[i2][1][j] == 1:
                            del A2[i2]
                    for i2 in range(len(A2)):
                        del A2[i2][1][j]
            else:
                if len(A2) == 0:
                    return [A[i][0]]
                else:
                    ret = alg(A2)
                    if len(ret):
                        ret = [A[i][0]] + ret
                        return ret

    return []


A = [['A', [1, 0, 0, 1, 0, 0, 1]] \
    , ['B', [1, 0, 0, 1, 0, 0, 0]] \
    , ['C', [0, 0, 0, 1, 1, 0, 1]] \
    , ['D', [0, 0, 1, 0, 1, 1, 0]] \
    , ['E', [0, 1, 1, 0, 0, 1, 1]] \
    , ['F', [0, 1, 0, 0, 0, 0, 1]]]

r = alg(A)

print(r)

A = [['1', [1, 1, 0, 0, 0, 0]] \
    , ['2', [0, 0, 0, 0, 1, 1]] \
    , ['3', [0, 0, 0, 1, 1, 0]] \
    , ['4', [1, 1, 1, 0, 0, 0]] \
    , ['5', [0, 0, 1, 1, 0, 0]] \
    , ['6', [0, 0, 0, 1, 1, 0]] \
    , ['7', [1, 0, 1, 0, 1, 1]]]

r = alg(A)

print(r)
