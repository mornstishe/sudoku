import sudoku_se
import time

t1 = time.time()
a = [l for l in sudoku_se.Sudoku('''008000000
    003100070
    100000032
    500703000
    009020000
    000000007
    000200003
    020005600
    060010080''')]
t2 = time.time()
print(t2 - t1)
print(len(a))
