import numpy as np
import matplotlib.pyplot as plt


# Group 33, variant 11
# Метод Стефенсена

# x є [-2;0]
# x^3 - x^2 + 3 = 0
# f`(x) = -2x + 3x^2
# x = (x^2 - 3)^1/3

def f(x_or_z): return x_or_z ** 3 - x_or_z ** 2 + 3


if __name__ == '__main__':
    e = 0.0000000000001
    old_x = -2
    x = old_x
    x = np.cbrt(x ** 2 - 3)

    while abs((x - old_x) / x) * 100 > e:
        old_x = x
        fx = f(x)
        z = x + fx
        fz = f(z)
        x = (x - (fx / (fz - fx)) * fx)
    print("x0 =", x)
    print("Перевірка:", x ** 3 - x ** 2 + 3)

    # Graph
    x_points = np.linspace(-2, 2)
    plt.grid()
    plt.scatter(x=x, y=0, color="black")
    plt.axhline(y=0, color="red", linestyle="dashed")
    plt.axvline(x=x, color="blue", linestyle="dashed")
    plt.plot(x_points, f(x_points), color="green")
    plt.title("f(x)")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()
