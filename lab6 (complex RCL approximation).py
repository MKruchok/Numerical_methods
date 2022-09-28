import copy
import numpy as np
import matplotlib.pyplot as plt
import time
import pandas as pd

# Constants
start_time = time.time()
C1 = 10 * 10 ** -3
C2 = 20 * 10 ** -3
L_max = 2
L_min = 0.2
I_min = 1
I_max = 2
R1 = 83
R2 = 93
R3 = 80
Umax = 10
a = 0.004
T = 2 * a
dt = T / 400

Uc1_old = 1
i2_old = 1
Uc2_old = 1
Uc1 = 1
i2 = 1
Uc2 = 1

n = 3
vals_x = []
uc1_vals_y = []
ul2_vals_x = []
ul2_vals_y = []
I2_vals = []
L2_vals = []
uc2_vals_y = []
u1_vals_y = []
u2_vals_y = []
t = 0

A = np.array(
    [
        [1, I_min, I_min ** 2, I_min ** 3],
        [1, I_max, I_max ** 2, I_max ** 3],
        [0, 1, 2 * I_min, 3 * I_min ** 2],
        [0, 1, 2 * I_max, 3 * I_max ** 2]
    ])
b = [L_max, L_min, 0, 0]


def U1(t):
    if t < a:
        return Umax / a * t
    elif a <= t < 2 * a:
        return -Umax / a * t + 10
    elif t == 2 * a:
        return 0
    else:
        return U1(t - T)


def U2():
    return i2 * R3


def _L2(i2):
    if abs(i2) <= I_min:
        return L_max
    if abs(i2) >= I_max:
        return L_min
    a = gauss()
    return a[0] + a[1] * abs(i2) + a[2] * i2 ** 2 + a[3] * abs(i2 ** 3)


def gauss():
    n1 = 4
    B = [L_max, L_min, 0, 0]

    x = 0
    v = copy.deepcopy(A)
    p = copy.deepcopy(B)
    y = [0 for _ in range(len(A))]
    c = [[0 for _ in range(n1)] for _ in range(n1)]

    for k in range(n1):
        # Column sort
        m = v[k][k]
        w = k
        for l in range(k + 1, n1):
            if m < abs(v[l][k]):
                m = abs(v[l][k])
                w = l
                p[k], p[w] = p[w], p[k]
                for d in range(n1):
                    v[k][d], v[w][d] = v[w][d], v[k][d]

        if v[k][k] != 0:
            y[k] = p[k] / v[k][k]
        else:
            y[k] = p[k]
        for i in range(k + 1, n1):
            p[i] -= v[i][k] * y[k]
            for j in range(k + 1, n1):
                c[k][j] = v[k][j] / v[k][k]
                v[i][j] -= v[i][k] * c[k][j]

        x = copy.deepcopy(y)
        for i in range(n1 - 1, -1, -1):
            s = 0
            for j in range(i + 1, n1):
                s += c[i][j] * x[j]
            x[i] = y[i] - s
    return x


def F(t, Uc1, i2, Uc2):
    fun = (U1(t) - Uc2) / C1
    return fun


def G(t, Uc1, i2, Uc2):
    fun = (Uc2 - i2 * (R2 + R3)) / _L2(i2)
    return fun


def H(t, Uc1, i2, Uc2):
    fun = ((U1(t) - Uc2) / C2) - i2
    return fun


def draw(vals_x, vals_y, title, xlabel, ylabel):
    vals_x = np.array(vals_x)
    vals_y = np.array(vals_y)
    plt.title(title, fontdict={'family': 'serif', 'color': 'darkred', 'size': 18})
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.axhline(y=0, color="black")
    plt.axvline(x=0, color="black")
    plt.plot(vals_x, vals_y, 'g')
    plt.show()


if __name__ == '__main__':
    while t <= 20 * T:
        K1 = dt * F(t, Uc1_old, i2_old, Uc2_old)
        L1 = dt * G(t, Uc1_old, i2_old, Uc2_old)
        M1 = dt * H(t, Uc1_old, i2_old, Uc2_old)
        K2 = dt * F(t + (dt / 3), Uc1_old + (K1 / 3), i2_old + (L1 / 3), Uc2_old + (M1 / 3))
        L2 = dt * G(t + (dt / 3), Uc1_old + (K1 / 3), i2_old + (L1 / 3), Uc2_old + (M1 / 3))
        M2 = dt * H(t + (dt / 3), Uc1_old + (K1 / 3), i2_old + (L1 / 3), Uc2_old + (M1 / 3))
        K3 = dt * F(t + dt * (2 / 3), Uc1_old + K2 * (2 / 3), i2_old + L2 * (2 / 3), Uc2_old + M2 * (2 / 3))
        L3 = dt * G(t + dt * (2 / 3), Uc1_old + K2 * (2 / 3), i2_old + L2 * (2 / 3), Uc2_old + M2 * (2 / 3))
        M3 = dt * H(t + dt * (2 / 3), Uc1_old + K2 * (2 / 3), i2_old + L2 * (2 / 3), Uc2_old + M2 * (2 / 3))
        Uc1 = Uc1_old + (K1 + 3 * K3) / 4
        i2 = i2_old + (L1 + 3 * L3) / 4
        Uc2 = Uc2_old + (M1 + 3 * M3) / 4

        vals_x.append(t)
        uc1_vals_y.append(Uc1)
        uc2_vals_y.append(Uc2)
        ul2_vals_y.append(i2)
        u1_vals_y.append(U1(t))
        u2_vals_y.append(U2())
        Uc1_old = Uc1
        i2_old = i2
        Uc2_old = Uc2

        t += dt
    i = 0
    while i <= I_max + 1:
        I2_vals.append(i)
        L2_vals.append(_L2(i))
        i += dt

    df = pd.DataFrame({
        "t": vals_x,
        "Вхідна напруга U1": u1_vals_y,
        "Вихідна напруга U2": u2_vals_y,
        "Напруга на С1": uc1_vals_y,
        "Напруга на L2": ul2_vals_y,
        "Напруга на С2": uc2_vals_y,
        "Час виконання": (time.time() - start_time)
    })
    np.savetxt("result.dat", df, fmt="%f", header="    T       U1       U2       Uc1      Ul2      Uc2   Runtime", comments="")

    draw(I2_vals, L2_vals, "L2(i2)", "i, А", "L, Гн")
    draw(vals_x, uc1_vals_y, "UС1", "t, сек", "U, В")
    draw(vals_x, ul2_vals_y, "UL2", "t, сек", "U, В")
    draw(vals_x, uc2_vals_y, "UС2", "t, сек", "U, В")
    draw(vals_x, u1_vals_y, "U1", "t, сек", "U, В")
    draw(vals_x, u2_vals_y, "U2", "t, сек", "U, В")
