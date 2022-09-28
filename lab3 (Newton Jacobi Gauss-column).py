import copy


# Group 33, variant 11
# Метод Ньютона з кінцево-різницевою матрицею Якобі
# (оберт.матриці методом Гауса з виб. гол. ел-тів по стовпцю)

# x1^2 + x2^2 + 0.1 -x1 = 0
# 2*x1*x2 + 0.1 - x2 = 0

# Поч. наближення: x1 = 0; x2 = 0;

def calculate_vect_f(args):
    return [f1(args), f2(args)]


def f1(args):
    x1, x2 = args
    return x1 ** 2 + x2 ** 2 + 0.1 - x1


def f2(args):
    x1, x2 = args
    return 2 * x1 * x2 + 0.1 - x2


if __name__ == '__main__':
    n = 2
    e = 0.00001
    h = 0.0001
    x = [0 for _ in range(n)]
    _x = [0 for _ in range(n)]
    f = [0 for _ in range(n)]
    _f = [0 for _ in range(n)]
    x_old = [0.5 for _ in range(n)]
    E = [[0 for _ in range(n)] for _ in range(n)]
    J = [[0 for _ in range(n)] for _ in range(n)]
    inverse = [[0 for _ in range(n)] for _ in range(n)]

    condition = False
    while not condition:
        f = calculate_vect_f(x)

        for i in range(n):
            for j in range(n):
                for k in range(n):
                    _x[k] = x[k]
                _x[j] = x[j] + h

                _f = calculate_vect_f(_x)
                J[i][j] = (_f[i] - f[i]) / h

        # Gauss:
        # Одинична матриця (identity matrix)

        for i in range(n):
            for j in range(n):
                if i == j:
                    E[i][j] = 1

        for b in range(n):
            # Прямий хід
            x = 0
            inx = [i for i in range(n)]
            v = copy.deepcopy(J)
            p = copy.deepcopy(E[b])
            y = [0 for _ in range(len(J))]
            c = [[0 for _ in range(n)] for _ in range(n)]

            for k in range(n):
                # Стовпцеві сортування
                m = v[k][k]
                w = k
                for l in range(k + 1, n):
                    if m > abs(v[k][l]):
                        m = abs(v[k][l])
                        w = l
                        p[k], p[w] = p[w], p[k]
                        for d in range(n):
                            v[k][d], v[w][d] = v[w][d], v[k][d]

                if v[k][k] != 0:
                    y[k] = p[k] / v[k][k]
                else:
                    y[k] = p[k]
                for i in range(k + 1, n):
                    p[i] -= v[i][k] * y[k]
                    for j in range(k + 1, n):
                        if v[k][k] != 0:
                            c[k][j] = v[k][j] / v[k][k]
                        else:
                            c[k][j] = v[k][j]
                        v[i][j] -= v[i][k] * c[k][j]

                # Обернений хід
                x = copy.deepcopy(y)
                for i in range(n - 1, -1, -1):
                    s = 0
                    for j in range(i + 1, n):
                        s += c[i][j] * x[j]
                    x[i] = y[i] - s


            for i in range(n):
                inverse[i][b] = x[i]

        # наступне наближення
        for i in range(n):
            s = 0
            for j in range(n):
                s += inverse[i][j] * f[j]
            x[i] = x_old[i] - s

        for i in range(n):
            if abs((x[i] - x_old[i]) / x[i]) * 100 < e:
                condition = True

        for i in range(n):
            x_old[i] = x[i]

    print("Корені:", x)
    print("Перевірка рівняння 1:", x[0] ** 2 + x[1] ** 2 + 0.1 - x[0])
    print("Перевірка рівняння 2:", 2 * x[0] * x[1] + 0.1 - x[1])
