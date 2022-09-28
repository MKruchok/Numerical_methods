import copy
import numpy as np


# Group 33, variant 11
# Знайти обернену матрицю методом Гауса з вибором гол. елемента по рядку

def gauss(a):
    # Одинична матриця (identity matrix)
    n = 4
    np.set_printoptions(suppress=True)
    e = [[0 for _ in range(n)] for _ in range(n)]
    inverse = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                e[i][j] = 1

    for b in range(n):
        # Прямий хід
        x = 0
        inx = [i for i in range(n)]
        v = copy.deepcopy(a)
        p = copy.deepcopy(e[b])
        y = [0 for _ in range(len(a))]
        c = [[0 for _ in range(n)] for _ in range(n)]

        for k in range(n):
            # Рядкові сортування
            m = v[k][k]
            w = k
            for l in range(k + 1, n):
                if m < abs(v[k][l]):
                    m = abs(v[k][l])
                    w = l
                    inx[k], inx[w] = inx[w], inx[k]
                    for d in range(n):
                        if d < k:
                            c[d][k], c[d][w] = c[d][w], c[d][k]
                        else:
                            v[d][k], v[d][w] = v[d][w], v[d][k]

            y[k] = p[k] / v[k][k]
            for i in range(k + 1, n):
                p[i] -= v[i][k] * y[k]
                for j in range(k + 1, n):
                    c[k][j] = v[k][j] / v[k][k]
                    v[i][j] -= v[i][k] * c[k][j]

            # Обернений хід
            x = copy.deepcopy(y)
            for i in range(n - 1, -1, -1):
                s = 0
                for j in range(i + 1, n):
                    s += c[i][j] * x[j]
                x[i] = y[i] - s

            # Впорядкування
            for i in range(n):
                if inx[i] != i:
                    z = inx[i]
                    value = x[i]
                    x[i] = x[z]
                    x[z] = value
                    inx[i] = inx[z]
                    inx[z] = z

        for i in range(n):
            inverse[i][b] = x[i]
    for i in range(n):
        print(inverse[i])
    # Перевірка
    check = np.array(a).dot(np.array(inverse))
    print(check)


if __name__ == '__main__':
    k = 11
    s = 0.02 * k

    a = [[8.3, 2.62 + s, 4.1, 1.9],
         [3.92, 8.45, 7.78 - s, 2.46],
         [3.77, 7.21 + s, 8.04, 2.28],
         [2.21, 3.65 - s, 1.69, 6.69]]

    gauss(a)
