import math
import matplotlib.pyplot as plt

# Group 33, variant 11
# Модифікований метод Ейлера (метод Ейлера з перерахунком)


def U1(u_max, f, t):
    return u_max * math.sin(2 * math.pi * f * t)


if __name__ == '__main__':
    u_max = 100
    f = 50
    R1 = 5
    R2 = 4
    R3 = 7
    L1 = 0.01
    C1 = 300 * 10 ** -6
    C2 = 150 * 10 ** -6
    t = 0
    h = 0.00001

    # x[0] = Uc1, x[1] = Uc2, x[2] = i2
    x_old = [0, 0, 0]
    x = [0, 0, 0]

    graph_x = []
    graph_y = []

    while t <= 0.2:
        x[0] = x_old[0] + h * ((U1(u_max, f, t) - x_old[0] + x_old[2] * R2 + x_old[2] * R2)
                               / (C1 * (R1 + R2 + R3)))
        x[1] = x_old[1] + h * (x_old[2] / C2)
        x[2] = x_old[2] + h * ((U1(u_max, f, t) - x_old[0] - x_old[1]
                                - R1 * ((U1(u_max, f, t) - x_old[0] + x_old[2] * R2 + x_old[2] * R2)
                                        / (R1 + R2 + R3))) / L1)
        x[0] = x_old[0] + ((0.5 * h) * (x_old[0] + x[0]))
        x[1] = x_old[1] + ((0.5 * h) * (x_old[1] + x[1]))
        x[2] = x_old[2] + ((0.5 * h) * (x_old[2] + x[2]))

        # U2 = i1 * R3 - i2 * R3
        U2 = (((U1(u_max, f, t) - x[0] + x[2] * R2 + x[2] * R2)
               / (R1 + R2 + R3)) * R3 - (x[2] * R3))
        graph_x.append(t)
        graph_y.append(U2)

        x_old[0] = x[0]
        x_old[1] = x[1]
        x_old[2] = x[2]
        t += h

    # Graph
    plt.title("Вихідна напруга ланки №11 (U2)")
    plt.xlabel("t, сек")
    plt.ylabel("U, В")
    plt.axhline(y=0, color="black")
    plt.plot(graph_x, graph_y, 'go', markersize=1, markevery=10)
    plt.show()
